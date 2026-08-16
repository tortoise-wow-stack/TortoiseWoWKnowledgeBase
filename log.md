# Directory Update Log

## 2026-08-16

* **PlayerBots overview:** Added a source-pinned, deployment-neutral [autonomy and limits](playerbots/autonomy.md) reference. It consolidates random-bot behavior, questing, vendor/AH/mail actions, activation gates, the separate AH market-maker, and known reliability limits without recording live deployment values.

## 2026-08-12

* **Credits:** Added prominent attribution to the original [Penqle/tortoise-wow](https://github.com/Penqle/tortoise-wow) project and the PlayerBots-enabled [Shyalya/tortoise-wow](https://github.com/Shyalya/tortoise-wow) fork used as the source-pinned documentation baseline.
* **Privacy boundary:** Removed the live deployment-state concept and sanitized host paths, aliases, account examples, topology/capacity observations, live counts/settings, incident artifacts, and deployment-specific commands. Runtime facts now come from an owner-supplied private record plus fresh read-only checks.
* **Portable operations:** Added deployment-neutral access, topology, backup/restore, extraction, build-hygiene, image-promotion/rollback, migration-validation, and capacity-measurement guidance distilled from private deployment experience.

* **Source-pinned documentation:** Replaced stale PlayerBots cheat-sheet claims and added [capability map](playerbots/capability-map.md), exact [`.bot`/`.rndbot` command reference](playerbots/console-commands.md), [plain-chat/parser](playerbots/chat-surface.md), complete [`@` audience-filter](playerbots/audience-filters.md), [action/strategy/query contracts](playerbots/actions-strategies.md), [addon/TCP transport](playerbots/addon-transport.md), [security/failure](playerbots/security-failures.md), [command-config](playerbots/command-config.md), [lifecycle](playerbots/bot-lifecycle.md), and [registry/count](playerbots/registry.md) documents.
* **Corrections:** Fixed rank-5+/console semantics for `!`, class-dependent role strategies, 137 trigger keys/129 destination commands, 16 debug strategies, normal-build action counts, `repop` action distinction, `.rndbot pid`, `.bot consums`, create/group/init parameters, whisper `queue` exclusion, `.bot debug` handler gating, async stats/login behavior, and internal-value vs command boundary.
* **Provenance:** PlayerBots baseline verified against source commit `172ee948e591f8bf1b53ea6389e3102186339f6e`; generated/verified `2026-08-12T10:15:00Z`. In-client addon packet delivery remains a residual verification item.

* **Schema lesson:** Documented the `character_inventory_copy` prerequisite and validation workflow without retaining a private incident timeline or artifact names.
* **Audit:** Reviewed the bundle against the official OKF v0.2 specification and source/live evidence, then retained only reusable deployment-agnostic conclusions.
* **Update:** Made `AGENTS.md` an OKF concept, repaired root index links, and clarified live-system safety and process-scoped health checks.

## 2026-08-11

* **Update**: Made the bundle deployment-agnostic (no PII — addresses, accounts, values moved to the owner's private deployment notes); added 9 groups: ops, tuning, playerbots, content-creation, client-side, history, references, integrations, workflows.
* **Update**: Added change-workflow playbook, codebase map, upstream link index, DB-migration workflow, fork fix-history, Turtle addon protocols, conditions/areatriggers, battlegrounds/PvP, config families, external integrations, housing/services, LLM-chat, bot factory/pool, performance, community docs (ike3).
* **Creation**: Established the OKF bundle: split the flat `Tortoise-WoW-Server.md` into concept documents across 9 groups.
* **Source**: Content derived from the flat reference built from 16 parallel research agents (source tree + live-server audits).
