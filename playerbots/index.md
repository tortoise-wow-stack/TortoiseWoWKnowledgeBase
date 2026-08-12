# PlayerBots — source baseline index

**Provenance:** commit `172ee948e591f8bf1b53ea6389e3102186339f6e`; generated and source-verified `2026-08-12T10:15:00Z`. Deployment settings and endpoints are intentionally excluded.

## Progressive disclosure

* [Capability map](capability-map.md) — start here: public/user-operable surfaces vs internal registries.
* [In-game usage](in-game-usage.md) — concise operator quickstart and corrected caveats.
* [`.bot` / `.rndbot` commands](console-commands.md) — exact aliases, parameters, target grammar, and return contracts.
* [Plain chat surface](chat-surface.md) — all 137 trigger keys, aliases, channels, parsing, and timing.
* [`@` audience filters](audience-filters.md) — complete filter families and examples.
* [Actions, strategies, and state queries](actions-strategies.md) — mutation syntax, role caveats, counts, and remote query formats.
* [Public action catalog](action-catalog.md) — generated exhaustive shared and class action registration names.
* [Strategy catalog](strategy-catalog.md) — generated exhaustive shared and per-class strategy registration names.
* [Addon transport](addon-transport.md) — `debug`, raw `CHAT_MSG_ADDON`, `#a`, TCP protocol, and security caveats.
* [Security and failures](security-failures.md) — ownership, ranks, gates, and exact important failures.
* [Command configuration](command-config.md) — switches that affect command behavior.
* [Offline alts vs random bots](bot-lifecycle.md) — login, self/always, random pool, and readiness.
* [Source registry](registry.md) — counts, internal-vs-public boundary, and compile-time conditions.

## Existing context

* [Architecture](architecture.md) — module layout and AI lifecycle.
* [Behavior systems](behavior-systems.md) — travel, questing, combat, professions, social, PvP, and groups.
* [Bot creation pipeline & random-bot pool](factory-pool.md) — creation phases and pool events.
* [Config](config.md) — broader `aiplayerbot.conf` inventory; command subset is [command config](command-config.md).
* [LLM & chat systems](llm-chat.md) — scripted speech and stubbed LLM integration.
* [Modification](modification.md) — code/SQL extension patterns (not a command list).
* [Performance](performance.md) — historical capacity notes; recheck runtime measurements separately.
* [Community docs](community-docs.md) — external lineage kept separate from this pinned source baseline.
