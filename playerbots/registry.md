---
type: Reference
title: PlayerBots source registry and build conditions
description: "Pinned source counts for chat triggers, strategies, actions, internal registries, and compile-time conditions."
tags: ["playerbots", "registry", "source"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


This is a count/audit aid, not a command list. Counts were generated from `creators["..."]` registrations at commit `172ee948e591f8bf1b53ea6389e3102186339f6e` and verified against the source paths below.

| Surface | Source file/context | Raw creators | Normal build | Build note |
| --- | --- | ---: | ---: | --- |
| Chat trigger keys | `strategy/triggers/ChatTriggerContext.h` | 137 | 137 | 129 distinct destination commands; aliases are documented in [chat](chat-surface.md) |
| Generic strategies | `strategy/StrategyContext.h` | 124 | 123 | `test` is `GenerateBotTests` only |
| Movement strategies | `MovementStrategyContext` | 7 | 7 | sibling context |
| Assist strategies | `AssistStrategyContext` | 3 | 3 | sibling context |
| Quest strategies | `QuestStrategyContext` | 2 | 2 | sibling context |
| Fish strategies | `FishStrategyContext` | 2 | 2 | sibling context |
| Generic action context | `actions/ActionContext.h` | 273 | 272 | `test` is `GenerateBotTests` only |
| Chat action context | `actions/ChatActionContext.h` | 128 | 128 | public chat action handlers |
| World-packet action context | `actions/WorldPacketActionContext.h` | 53 | 53 | packet-driven action names |
| Shared action union | the three shared action contexts | 454 source-visible creators | 451 source-visible unique names | normal build excludes conditional `test`: 450 unique |
| Class action registrations | ten class `*AiObjectContext.cpp` files | 712 registrations | 675 unique names | a bot receives only its compiled class context |
| Complete action source union | shared + class action contexts | 1166 registrations | 1126 unique names | source-visible, not one bot's runtime surface; exhaustive names in [action catalog](action-catalog.md) |
| Generic triggers | `triggers/TriggerContext.h` | 256 | 256 | internal strategy event triggers; not plain chat commands |
| World-packet triggers | `triggers/WorldPacketTriggerContext.h` | 54 | 54 | internal packet triggers |
| Values | `strategy/values/ValueContext.h` | 332 | 332 | internal/diagnostic value creators; not commands |
| Remote query names | `PlayerbotAI::HandleRemoteCommand` | 11 exact + budget family | 11 exact + budget family | not an object registry; response contracts are in [actions](actions-strategies.md) |
| Class strategy registrations | ten class `*AiObjectContext.cpp` files | 778 registrations | 643 unique names | duplicates occur within/across contexts; Classic excludes 11 death-knight names |
| Complete strategy source union | shared/sibling + class strategy contexts | source registrations vary by conditional blocks | 767 unique names | source-visible union; exhaustive names in [strategy catalog](strategy-catalog.md) |

The source module CMake sets `CMANGOS` and `MANGOSBOT_ZERO` for the default module path; `MANGOSBOT_ONE/TWO` are alternate expansion conditionals. Therefore DK-only keys and other expansion-gated action/race/class keys must be marked conditional. Counts do not imply every strategy/action is possible for every bot: class, state, prerequisites, gear, map, packet, and security checks apply.

## Source anchors

* Commands/targeting/handlers: `PlayerbotMgr.cpp:229-289`, `823-1088`, `1450-1870`, `2100-2205`, `2259-2900`, `3088-3235`.
* Random commands: `RandomPlayerbotMgr.cpp:3589-3734`, `4508-4546`.
* Chat triggers/parser: `ChatTriggerContext.h`, `ExternalEventHelper.h`, `PlayerbotAI.cpp:1466-1614`.
* Filters: `ChatFilter.cpp` composite filter classes.
* Remote query API: `PlayerbotAI.cpp:6642-6973`.
* Transport: `PlayerbotCommandServer.cpp`; startup gate in `RandomPlayerbotMgr.cpp:268-272`.

To discover what a running build actually exposes, prefer its `.bot help commands`, `help commands`, and source/build flags over copying a count from another expansion.
