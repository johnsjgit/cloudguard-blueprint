# CloudGuard Blueprint

A small, vendor-neutral reference project for designing **AI-ready cloud workloads** without exposing secrets, endpoints, or customer data.

## Why this exists

Cloud and AI projects often begin with a diagram and end with configuration scattered across code, chats, and local files. This repository keeps the security conversation at the start: validate a reference configuration before any infrastructure is provisioned.

## What it demonstrates

- Configuration-first design with no live cloud dependencies
- Secrets referenced by a manager, never embedded in code or configuration
- Private-by-default network posture
- Encryption, audit logging, and data-classification guardrails
- AI controls for grounding, prompt-injection review, PII handling, and human oversight

## Project structure

    src/                 # Standard-library validation CLI
    examples/            # Safe sample configuration
    README.md            # Architecture and local usage

## Quick start

    python src/security_check.py examples/reference-config.json

The command reports configuration guardrails. It does not authenticate to a cloud account, create resources, or transmit data.

## Reference architecture

    User / application
            |
            v
    Private application boundary
            |
            +--> AI gateway: input policy, grounding, output review
            +--> Data boundary: classified data, encryption, retention controls
            +--> Observability: audit logs and alerts
            +--> Secrets manager: references only, never hard-coded credentials

## Security principles

1. **No secrets in Git.** Use environment variables or a managed secret store at runtime.
2. **Least privilege.** Give each workload only the permissions it needs.
3. **Private by default.** Expose a public endpoint only when there is a documented need and a compensating control.
4. **Traceability.** Log security-relevant events without logging sensitive prompt or customer data.
5. **Human accountability.** Treat AI output as an assistive capability, not an unreviewed production decision.

## Scope

This is a portfolio and learning reference, not a production deployment template. The configuration is deliberately generic and contains no tenant IDs, database addresses, keys, customer data, or live cloud resources.

## License

MIT — see [LICENSE](LICENSE).
