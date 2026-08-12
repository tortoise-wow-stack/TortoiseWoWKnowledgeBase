---
type: Reference
title: Logs, monitoring & recovery
description: Log locations, current-process health, performance tools, crash loops, migrations, and disk growth.
tags: [ops, logs, recovery]
resource: file:///opt/turtle/logs
status: stable
generated: { by: pi/agent, at: 2026-08-12T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
  - id: packaging
    resource: https://github.com/Nescabir/tortoise-docker
    title: Tortoise Docker packaging
---
**Related:** [Access & status](/ops/access-status.md) · [Server rates & limits](/tuning/rates-limits.md) · [DB migrations](/content-creation/db-migrations.md)

## Logs, monitoring, recovery

- Container-internal world logs live under `/opt/turtle/logs`; common outputs include per-start server logs, `errors.log`, bot events, loot, level-up, and performance logs. Determine rotation and retention from the deployment rather than assuming either exists.
- `LogLevel`, `LogFileLevel`, `LogSQL`, and per-domain filters control verbosity. Raise them temporarily for diagnosis, then restore a measured baseline because bot and SQL logging can grow rapidly.
- World performance tools: `.perf enable on`, `.perf intervalreport <seconds>`, `.perf cpu`, `.perf memory`, and `.perf resources`. PlayerBots has a separate performance monitor; see [PlayerBots performance](/playerbots/performance.md).
- Compose restart policies may restart a crashed process automatically. A persistent startup failure therefore becomes a restart loop and can create one log per attempt. Inspect current restart counts and the first fatal trace before giving generic restart advice.
- Readiness is process-scoped: require `World server is up and running` after the current container's `StartedAt`; an old line is not health evidence.
- `AutoRestart.*`, honor-maintenance settings, and `BackupCharacterInventory` are deployment configuration. When inventory backup is enabled, the character schema must contain `character_inventory_copy` compatible with `character_inventory`; the code truncates and refills that table during maintenance.
- The initializer imports the base schema and packaged updates unless the initialization marker says it already ran. The boot-time updater tracks migration name and hash. Verify actual packaged coverage after each rebuild; do not infer character-schema migration support from the presence of a migrations table alone.
- Error-tolerant SQL import can produce a final completion line after an earlier failed statement. Preserve the full log, inspect errors, assert required tables/columns and migration hashes, and then prove current-process world readiness.
- Watch both log volumes and extracted-data/backup storage. Define retention explicitly and test recovery through an isolated restore rather than relying on file existence.
