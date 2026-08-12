---
type: Reference
title: DB migrations & SQL workflow
description: How schema and content changes are tracked, validated, shipped, and recovered across realm databases.
tags: [content, db, migrations]
resource: mariadb://<world-db>/migrations
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

**Related:** [Change workflow](/workflows/change-playbook.md) · [Hot-reload commands](/ops/reloads.md) · [Logs, monitoring & recovery](/ops/logs-monitoring.md)

## How migrations work

- Timestamped update files under `sql/database_updates/` use names such as `<yyyymmddhhmmss>_<realm>.sql`. Recount and inspect the actual source/image after rebuilding; branches and packaging can change.
- Migration tables store the update identifier/name, uppercase SHA-1 hash, and application time. With database auto-update enabled, the world process applies updates whose name and hash are not recorded before completing startup.
- Verify routing per database. The presence of a character/logon migration table or a filename suffix does not prove both the initializer and C++ updater deliver that file to the intended schema.
- `BackupCharacterInventory = 1` requires a character-schema table `character_inventory_copy` compatible with `character_inventory`; maintenance truncates and repopulates it. Package the prerequisite in fresh-install schema and a tested upgrade path.
- Restored dumps can conflict with packaged migration history. Before first restored startup, compare the dump's migration records with the update files to avoid replaying already-materialized DDL or content.

## Initialization validation

The packaging initializer may execute SQL in an error-tolerant mode. A zero exit status or final “complete” line is therefore insufficient by itself.

1. Preserve the complete initializer log.
2. Inspect every SQL error and classify only explicitly documented idempotent cases as tolerated.
3. Assert required databases, tables, columns, indexes, and migration name/hash records.
4. Start the world and require a readiness line from the current process.
5. Perform a login and restart-persistence check before treating the database as durable.

The first database may be considered disposable only until those checks pass. Once accounts or characters matter, take a checksum-verified dump before any reset.

## Shipping a schema or content change

1. Direct SQL plus `.reload <table>` is suitable for an intentional one-off deployment change when the table supports reload and the operation is recorded privately.
2. A world change that must survive fresh installation belongs in a timestamped world update and the relevant base schema when appropriate.
3. A character or logon schema change needs both fresh-install coverage and a migration route proven end to end through the actual packaging. Do not assume suffix support.
4. Boot-loaded tables such as `spell_template`, `faction`, `faction_template`, `skill_line_ability`, and `gameobject_template` require a world restart after application.
5. Before release, restore a representative dump into an isolated database, apply the candidate image, verify migration state, require current-process readiness, and run the affected in-game check.

## Authoring tools

- `sql/tools/make_migration.bat` and `sql/tools/touch_migration.sh` scaffold update files.
- `sql/tools/probe_migration_overlap.py` and its report detect duplicate-key overlap between update files.
- Scripts under `sql/tools/` are manual helpers; inspect assumptions and identifiers before running them against a deployment.

Completion: fresh install and representative restore both reach the same intended schema/content state, with matching migration hashes and a successful current-process startup.
