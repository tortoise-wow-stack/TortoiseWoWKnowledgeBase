---
type: Reference
title: Persistence map
description: Which configuration changes survive container recreation and how render-time overrides interact.
tags: [ops, persistence]
status: stable
generated: { by: pi/agent, at: 2026-08-12T12:00:00Z }
sources:
  - id: packaging
    resource: https://github.com/Nescabir/tortoise-docker
    title: Tortoise Docker packaging
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---
**Related:** [Env-driven config](/tuning/env-config.md) · [Server rates & limits](/tuning/rates-limits.md)

## Persistence map

The packaging entrypoint renders configuration on every container start. It creates a working `.conf` from the image's `.conf.dist` when needed, then overwrites every environment-mapped key. Container-internal config files live in the writable container layer unless a deployment mounts them.

**Ways to change a value, ranked by permanence:**

1. **Private `.env` + `docker compose up -d`** — supported for render-mapped keys and survives recreation. Keep secrets out of logs, build contexts, and documentation.
2. **Packaging render script + image rebuild** — add a render mapping in the Compose checkout when a key should become an environment-managed deployment value. Record and test the packaging change.
3. **Bind-mount a config file** — appropriate for keys without environment mappings. The render script edits configured keys at startup, so a read-only mount can fail under `set -euo pipefail`; either make the render path compatible with read-only input or use a controlled writable/generated file.
4. **Database change** — persists in the database volume and must be represented by a tested migration or documented one-off operation when it must survive a fresh install.
5. **Raw edit inside a running container** — diagnostic only. Recreation removes it, and render-mapped values may be overwritten on the next start.

The reference stack uses separate persistence boundaries for database data, the one-shot initialization marker, logs, and the client-derived data mount. Treat database data plus its initialization marker as one reset boundary. The client-derived data should be mounted read-only at `/opt/turtle/data`; its host path is deployment-specific.

Completion for any persistent config change: recreate the affected service, prove current-process readiness, inspect the rendered value without printing secrets, then recreate it once more to prove the value survives.
