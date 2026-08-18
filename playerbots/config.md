---
type: Reference
title: PlayerBots config
description: Source-oriented aiplayerbot.conf families for population, timing, behavior, talents, and AhBot.
tags: [playerbots, config]
resource: file:///opt/turtle/etc/aiplayerbot.conf
status: stable
generated: { by: pi/agent, at: 2026-08-18T17:00:00Z }
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

## Activity modes (always-active vs priority brackets)

`AiPlayerbot.DisableActivityPriorities` selects between two scheduling modes. **This fork ships it uncommented at `1` in the `.dist`**, so a stock build runs everything at full speed.

- **Mode 2 (value `0`, upstream default):** the activity-priority system assigns each bot a priority bracket. Bots near a real player or with a master run at full cadence (`ReactDelay`, default 100 ms); the bottom bracket is throttled to `PassiveDelay` (default 10 s) with movement-only work, and distant bots are what the "activity scaling" guard optimizes.
- **Mode 1 (value `1`):** every bot is forced into the top activity class (priority type `HAS_REAL_PLAYER_MASTER` per the module maintainer), so all bots run full-speed everywhere and `botActiveAlone` is ignored. AI cost then scales linearly with online bots; the fork's own `.dist` comment says to reduce the population if lags appear rather than rely on optimizations.

`AiPlayerbot.botActiveAlone` is the percentage of fully active **bottom-bracket** bots only (`priorityBracket.second == 100` per the module maintainer; bracket internals not re-verified at the pinned baseline). Bots in any higher bracket stay active regardless of the setting — which is why raising it appears to do nothing on busy realms. On a solo/low-traffic realm, where most distant bots sit in the bottom bracket, it is the effective "background world life" dial between idle and always-active behavior.

## Chat and broadcast throttling

- `EnableBroadcasts` (default 1) is the master switch. `BroadcastToWorldGlobalChance` / `BroadcastToGeneralGlobalChance` (and trade/LFG/local-defense variants) are 0–30000 per-message chances; the `.dist` documents the two global gates as **the main throttle** on visible chat spam — kill/level-up/suggest broadcasts route through them at chance 100.
- `BroadcastChanceSuggestSomething` (default 2000) was cut upstream from 100% because it was the single largest source of world/general noise.
- Reply chances (`ToxicLinksRepliesChance`, `ThunderfuryRepliesChance`, `GuildRepliesRate`) and `RandomBotSayWithoutMaster` (bots speak master-directed lines unprompted) add further chatter; gate them at 0 to silence, or use `EnableBroadcasts = 0` to stop broadcasts entirely.
- `AllowedLogFiles` selects per-action CSV logging (`bot_events.csv`, `deaths.csv`): every bot action writes a row, so it is per-bot CPU/I/O overhead — reduce it when running large populations (see [logs & monitoring](/ops/logs-monitoring.md)).

## Fresh level-1 starts

- `DisableRandomLevels = 1` + `randombotStartingLevel = 1` makes every created bot begin at the starting level and work up — but **only while the realm runs**; a stopped-and-started realm leaves the pool stuck at that level.
- **`RandomBotMaxLevelChance` (default 0.15) still applies on first randomize** — 15% of a "level-1" pool spawns at max level unless it is set to 0.
- The level-1 teleport bucket holds only 247 points, all in starting zones (`.dist` documentation): a fresh level-1 pool crowds into the six racial starting zones until the curve grows; raising the starting level does not help, because one shared level means one shared bucket.
- Flipping `DisableRandomLevels` on an existing realm does not re-level the pool — `Randomize()` reassigns levels and would destroy an organic curve. Use the pool reset recipe in [admin recipes](/ops/admin-recipes.md).

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
