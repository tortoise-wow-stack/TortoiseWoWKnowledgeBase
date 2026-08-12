---
type: Reference
title: PlayerBots config
description: Source-oriented aiplayerbot.conf families for population, timing, behavior, talents, and AhBot.
tags: [playerbots, config]
resource: file:///opt/turtle/etc/aiplayerbot.conf
status: stable
generated: { by: pi/agent, at: 2026-08-12T12:00:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e
    title: Tortoise WoW source at the pinned PlayerBots baseline
---
**Related:** [PlayerBots modification](/playerbots/modification.md) · [PlayerBots performance](/playerbots/performance.md) · [Persistence map](/ops/persistence.md)

## PlayerBots configuration (`aiplayerbot.conf`)

The container-internal file is `/opt/turtle/etc/aiplayerbot.conf`. Its host persistence mechanism is deployment-specific. Treat the image's `.conf.dist` at the pinned source/image as the default authority; do not copy a live deployment's values into this bundle.

## Population and lifecycle

| Key family | Purpose |
| --- | --- |
| `AiPlayerbot.MinRandomBots` / `MaxRandomBots` | Target online random-bot population; commonly render-mapped from `.env` |
| `RandomBotMinLevel` / `RandomBotMaxLevel` | Eligible generated/randomized level range |
| `RandomBotAutoCreate` / `RandomBotAccountCount` | Character-pool creation policy and account count |
| `RandomBotMaps` | Maps eligible for random bots |
| `RandomBotUpdateInterval` | Random-bot manager update cadence, not each bot's full AI reaction cadence |
| `RandomBotsMaxLoginsPerInterval` | Login throttling |
| `RandomBotCountChangeMinInterval` / `MaxInterval` | Population re-evaluation window |
| `RandomBotLoginWithPlayer` | Restrict random-bot presence to periods with a real player online |
| `DisableActivityPriorities` | Force always-active scheduling when enabled; an important CPU lever |

The size of an offline character pool is not an online-bot capacity target. Measure online population on the target deployment; see [performance](/playerbots/performance.md).

## Behavior and timing

| Key family | Purpose |
| --- | --- |
| `ReactDelay`, `PassiveDelay`, `RepeatDelay`, `RpgDelay` | AI scheduling and pacing |
| `SightDistance`, `SpellDistance`, `HealDistance` | Perception/action ranges |
| `CombatStrategies`, `RandomBotCombatStrategies`, `NonCombatStrategies` | Default strategy sets |
| `AutoEquipUpgradeLoot`, `AutoPickTalents` | Gear and talent automation |
| `BotCheats`, `RndBotCheats` | Explicit bot-only assistance; review before enabling |
| `XPRate`, starting-level and level-sync families | Bot progression |
| `EnableBroadcasts`, `InviteChat` | Social and invitation behavior |
| `IterationsPerTick`, `AsyncBotLogin` | Work bounds and login scheduling |

## Premade talent specs

```ini
AiPlayerbot.PremadeSpecName.<class>.<spec> = <name>
AiPlayerbot.PremadeSpecProb.<class>.<spec> = <weight>
AiPlayerbot.PremadeSpecLink.<class>.<spec>.<level> = <talent-link>
```

Links contain the three talent-tree digit runs and are validated at boot. An invalid level entry is skipped. Generate them with `tools/talents/build_premade_specs.py --dbc <dbc-dir> --rate <rate>` and keep `--rate` aligned with `Rate.Talent`.

## AhBot

The `AhBot.*` family controls the supported auction-house bot and requires an eligible character GUID when enabled. The older `AuctionHouseBot.*` family is separate legacy configuration. Verify the source/image before enabling either.

Completion for a config change: persist it through the deployment's supported config path, recreate `mangosd`, prove current-process readiness, inspect the rendered value without exposing secrets, and test the intended bot behavior in-game.
