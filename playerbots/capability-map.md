---
type: Reference
title: PlayerBots capability map
description: "Source-verified map of public and user-operable PlayerBots surfaces; internal registries are clearly separated from commands."
tags: ["playerbots", "capability-map"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


**Baseline:** source commit `172ee948e591f8bf1b53ea6389e3102186339f6e`. This document is the progressively disclosed map. Start here, then follow the deep references below.

## Choose a surface

| Need | Entry point | Deep reference |
| --- | --- | --- |
| Operate an owned or random bot | `.bot` / `.rndbot` | [console commands](console-commands.md) |
| Send a natural-language command | Plain SAY/YELL/WHISPER/PARTY/RAID/GUILD chat | [chat surface](chat-surface.md) |
| Select a subset of bots | Leading `@` filter in chat | [audience filters](audience-filters.md) |
| Query a bot for addon state | `debug <query>` or TCP `query,guidLow` | [addon transport](addon-transport.md) |
| Execute one action or inspect output | `.bot do`, `.bot cmd`, `record/read/clear` | [actions and contracts](actions-strategies.md) |
| Change persistent/runtime behavior | `co`, `nc`, `de`, `react`, `all`; config | [actions and strategies](actions-strategies.md), [config](command-config.md) |
| Understand who may control whom | Ownership, group, guild, rank, level/gear gates | [security and failures](security-failures.md) |
| Distinguish offline alts from random bots | `.bot always` vs random pool | [lifecycle](bot-lifecycle.md) |

## What is public vs internal

* **Public/user-operable:** `.bot` and `.rndbot` handlers; chat trigger names; `d/do` action names; `co/nc/de/react/all`; `@` filters; the 11 exact remote state-query names plus the `budget` prefix family; chat/TCP transport behavior; configuration switches documented in [command config](command-config.md).
* **Internal, not commands:** `ValueContext` names, generic/class `TriggerContext` names, strategy trigger nodes, action implementation classes, and AI object names. `debug values` exposes a diagnostic dump but does not turn every value into a supported command. Do not advertise `AI_VALUE` names as user syntax.
* **Build conditions matter:** normal source registries include 137 chat triggers, 123 generic strategies, 450 normal-build action names across the three public action contexts, and 11 exact remote query names plus `budget` prefix handling. `test` strategy/action and `.bot runtest` are only present under `GenerateBotTests`; see [registry](registry.md). Class-specific strategy keys are additional and selected by class contexts.

## Operational truth in one paragraph

Chat commands are usually queued to the bot AI tick; `debug <query>` is synchronous and emits a `CHAT_MSG_ADDON` packet. `.bot do` captures synchronous action output, while `.bot cmd` queues a parsed chat command. Add/login returns before the bot is necessarily in-world. Human-readable bot replies can be delayed, suppressed by `silent`, deduplicated, or absent on failure. Addon authors should use exact query responses only where this baseline marks them as stable enough, and treat all other text as display-oriented.

## Provenance and verification

The source commit is immutable provenance for this baseline; generated and verified at `2026-08-12T10:15:00Z`. Source paths and line-oriented behavior are linked from each focused document. In-client verification remains required for client event delivery of raw `CHAT_MSG_ADDON` debug responses and `#a` PARTY/LANG_ADDON replies.
