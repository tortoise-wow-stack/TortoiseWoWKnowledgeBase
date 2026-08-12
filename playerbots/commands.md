---
type: Cheat Sheet
title: PlayerBots command reference
description: Complete source-baseline map of PlayerBots commands, triggers, filters, transport, and diagnostics.
tags: ["playerbots", "commands"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


This former cheat sheet is now a concise router. The complete current baseline is split into focused documents so command syntax is not confused with internal AI values:

* [Capability map](capability-map.md) — choose an entry point and distinguish public surfaces from internals.
* [`.bot` / `.rndbot` commands](console-commands.md) — exact handlers, aliases, parameters, targets, and return strings.
* [Plain chat](chat-surface.md) — 137 trigger keys, 129 destination commands, parsing, channels, and timing.
* [`@` audience filters](audience-filters.md) — role, level, group, guild, class, race, item, quest, location, probability, and state filters.
* [Actions, strategies, and state queries](actions-strategies.md) — build-conditional registries, `do` behavior, `co/nc/de/react/all`, and remote query response formats.
* [Public action catalog](action-catalog.md) and [strategy catalog](strategy-catalog.md) — exhaustive generated registration names at the pinned commit.
* [Addon transport](addon-transport.md) — `debug`/`CHAT_MSG_ADDON`, `#a`, TCP framing, and addon limitations.
* [Security and failures](security-failures.md) — ownership ladder and exact important failures.
* [Command config](command-config.md) — switches affecting routing, persistence, timing, summon, and listener startup.
* [Offline alts vs random bots](bot-lifecycle.md) — ownership and asynchronous lifecycle distinctions.
* [Registry/count notes](registry.md) — source counts, build conditionals, and internal-vs-public registry boundaries.

**Corrected baseline highlights:** `!` requires rank strictly above rank-4 `SEC_GAMEMASTER` in this port (rank 5/6); `co +tank/+heal/+dps` are class-dependent; chat triggers are 137 keys/129 destination commands; `repop` is a `do` action, not a chat trigger; `debug*` strategies count 16; normal-build public action union is 450 unique names; `.rndbot pid`, `.bot consums`, create/group/init parameters, `logout cancel`, whisper `queue` exclusion, raw addon/TCP transport, and `@` filters are documented in the focused pages.

**Provenance:** all source claims above are pinned to commit `172ee948e591f8bf1b53ea6389e3102186339f6e`, generated and source-verified `2026-08-12T10:15:00Z`. In-client verification remains needed for Turtle client delivery of `CHAT_MSG_ADDON` and PARTY/LANG_ADDON compatibility replies.
