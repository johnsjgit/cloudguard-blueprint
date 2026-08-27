"""Validate a safe reference configuration for an AI-ready cloud workload."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def value_at(config: dict[str, Any], *keys: str) -> Any:
    current: Any = config
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def validate(config: dict[str, Any]) -> list[str]:
    """Return human-readable guardrail failures for a reference config."""
    expected = {
        ("network", "public_access"): False,
        ("secrets", "inline_values"): False,
        ("security", "encryption_at_rest"): True,
        ("security", "encryption_in_transit"): True,
        ("security", "least_privilege"): True,
        ("logging", "audit_enabled"): True,
        ("logging", "sensitive_payload_logging"): False,
        ("ai", "grounding_enabled"): True,
        ("ai", "pii_redaction"): True,
        ("ai", "human_review_required"): True,
    }
    failures = []
    for path, expected_value in expected.items():
        actual = value_at(config, *path)
        if actual is not expected_value:
            failures.append(
                f"{'.'.join(path)} must be {str(expected_value).lower()} "
                f"(found {actual!r})"
            )

    provider = value_at(config, "secrets", "provider")
    if provider != "managed-secret-store":
        failures.append("secrets.provider must be 'managed-secret-store'")

    classification = value_at(config, "data", "classification")
    if classification not in {"internal", "confidential", "restricted"}:
        failures.append("data.classification must be internal, confidential, or restricted")
    return failures


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python security_check.py <reference-config.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Cannot read configuration: {error}", file=sys.stderr)
        return 2

    failures = validate(config)
    if failures:
        print("Guardrail check failed:")
        print(*[f"- {failure}" for failure in failures], sep="\n")
        return 1

    print("Guardrail check passed: configuration meets the reference controls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
