---
type: Reference
title: PlayerBots command-related configuration
description: "Source-verified configuration switches that alter command routing, targeting, security, persistence, timing, and addon transport."
tags: ["playerbots", "config", "commands"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


Defaults below are source defaults from `PlayerbotAIConfig.cpp` at `172ee948e591f8bf1b53ea6389e3102186339f6e`; distribution comments may show deployment examples, not guarantees. This bundle intentionally omits deployment values.

| Key | Source default | Effect |
| --- | --- | --- |
| `AiPlayerbot.Enabled` | source default is read from config; distribution enables it for this checkout | disables all PlayerBots handlers when false |
| `AiPlayerbot.CommandPrefix` | empty | when non-empty, every plain chat command must begin with it |
| `AiPlayerbot.CommandSeparator` | `\` | splits stacked chat commands recursively |
| `AiPlayerbot.AllowGuildBots` | true | permits guild ownership path for bots outside caller account |
| `AiPlayerbot.AllowMultiAccountAltBots` | true | permits cross-account alt bots when guild conditions pass |
| `AiPlayerbot.NonGmFreeSummon` | false | permits the summon action's free-summon path to non-player security; account/random/master ownership checks still apply to `.bot summon` |
| `AiPlayerbot.SelfBotLevel` | `GM_ONLY` (numeric default from enum) | controls `.bot self` / `.bot always` offline AI policy |
| `AiPlayerbot.ExplicitDbStoreSave` | false | when true, strategy changes such as `co`/`nc` do not auto-save to DB store; use explicit save behavior instead |
| `AiPlayerbot.NonCombatStrategies` | `+return,+delayed roll` in code default (distribution may override) | default non-combat strategy changes and claims about always-on behavior |
| `AiPlayerbot.RandomBotNonCombatStrategies` | `+custom::say` in code default | random-pool non-combat additions |
| `AiPlayerbot.UseWanderAsDefaultFollowStrategy` | true | bots without an active player master default to `wander`; the factory uses this to choose wander vs follow defaults |
| `AiPlayerbot.RandomBotInvitePlayer` | true | allows nearby random bots to invite real players; also affects some invite/guild actions |
| `AiPlayerbot.RandomBotGroupNearby` | true | enables nearby random-bot grouping behavior |
| `AiPlayerbot.ReactDelay` | 100 ms | AI tick floor and queued-command latency |
| `AiPlayerbot.RepeatDelay` | 5000 ms | suppresses duplicate tells/actions within the interval |
| `AiPlayerbot.CommandServerPort` | 0 | TCP command server disabled at zero; nonzero starts the unauthenticated all-interface listener when manager startup gates pass |
| `AiPlayerbot.RandomBotAutologin` | true | required with enabled subsystem for RandomPlayerbotMgr constructor to start the command server |
| `AiPlayerbot.WhisperDistance` | source default is a large 6000.0 in the audit context | distance gate for free-bot whispers; verify build/config before relying on it |

Other behavior config (strategies, cheats, questing, LFG/BG, broadcasts) changes what commands can do, but does not expand the public grammar. Reloading config via `.bot reload` is GM-gated; source behavior after reload should be rechecked in-client.
