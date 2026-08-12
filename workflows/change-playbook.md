---
type: Playbook
title: Change workflow (the golden path)
description: Decision tree for making any change — config, SQL, C++, or client DBC — with the verify loop for each.
tags: ["workflows", "playbook"]
status: stable
generated: { by: pi/agent, at: 2026-08-11T18:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [Persistence map](/ops/persistence.md) · [Hot-reload commands](/ops/reloads.md) · [Codebase map](/references/codebase-map.md) · [DB migrations](/content-creation/db-migrations.md)

## Decide where the change lives

| What you want to change | Where | Apply via | Verify |
| --- | --- | --- | --- |
| Server value (rates, limits, toggles) | `mangosd.conf` | `.env` if render-mapped, else bind-mount (§6 persistence) + restart | world-ready line; `.perf` for perf |
| Bot behavior value | `aiplayerbot.conf` | bind-mount + recreate mangosd | bot logs / `.rndbot stats` |
| Content (NPC, quest, item, GO, loot, gossip, vendor, event) | tw_world tables | SQL + `.reload <table>` | in-game check; `.lookup` / `.npc info` |
| Spell data | `spell_template` (+ `spell_effect_mod`, `locales_spell`) | SQL + **restart** (no reload) | `.learn <id>` then cast |
| Talents / skill base / faction defs | DBC (`Talent.dbc`…) / `faction` tables | client patch / SQL + **restart** | in-game UI |
| Boss mechanics, scripts, new strategies | C++ (`src/scripts/`, `src/game/`, PlayerBots module) | rebuild image + recreate | logs + in-game test |
| Client visuals (icons, models, tooltips) | client DBC via patch MPQ | drop `patch-<single-char>.mpq` into Data/ | client shows it |

## The verify loop (every change)

1. **DB edits:** run the SQL, then `.reload <table>` or restart where required. Confirm with a read-only query and an in-game check.
2. **Config edits:** persist the change through the deployment's supported path, recreate the affected service, and require a readiness line from the current process.
3. **C++ edits:** build a traceable candidate image, preserving packaging/source commits, arguments, toolchain, and digest. Test boot and the affected behavior against an isolated restored database before promotion.
4. **Data safety:** use the owner-approved backup command before destructive SQL. Require a checksum-verified dump and never reset database data separately from its initialization marker.
5. **Promotion:** after restore/startup and in-game tests pass, pin the candidate image/source in the private deployment configuration and retain the last known-good image for rollback.
6. **Persistence:** recreate the service again and prove the intended config, schema, and behavior survive. Raw in-container edits are diagnostic only.

## Rules of thumb for agents

- Prefer SQL + reload over restart; prefer restart over rebuild.
- The server reloads 70+ tables live — most content work never needs a restart.
- `spell_template`, `faction`, `faction_template`, `skill_line_ability`, `gameobject_template` load only at boot.
- Client build gate is 7272. Image selection is deployment-specific: validate CPU compatibility, pin the tested image/source, and preserve rollback.
- When in doubt about where a value lives: `grep` the source for the config key, or `DESCRIBE` the table.
