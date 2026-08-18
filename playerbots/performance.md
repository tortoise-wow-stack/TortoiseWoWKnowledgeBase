---
type: Reference
title: PlayerBots performance & capacity
description: Source-derived cost model, tuning levers, and a deployment-neutral measurement procedure.
tags: [playerbots, performance, capacity]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-18T17:00:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at the pinned baseline
---

**Related:** [PlayerBots config](/playerbots/config.md) · [PlayerBots architecture](/playerbots/architecture.md) · [Logs, monitoring & recovery](/ops/logs-monitoring.md)

## Cost model

Performance scales primarily with **online bots × activity**, not with the number of character rows available in the random-bot pool. Each online bot evaluates triggers, cached values, and candidate actions on its AI schedule; active combat bots cost more than distant or passive bots. Login, randomization, pathing, and travel-cache work can add temporary spikes.

Do not copy a bot-count ceiling from another machine. CPU generation, core allocation, co-tenants, maps, player proximity, active strategies, and configuration all change the result.

## High-impact levers

1. **`AiPlayerbot.DisableActivityPriorities = 0`** — allows idle/distant bots to use lower-activity scheduling instead of forcing every bot through always-active work.
2. **`AiPlayerbot.ReactDelay`** — increasing it reduces active decision frequency at the cost of slower reactions.
3. **`AiPlayerbot.PassiveDelay`** — controls low-activity scheduling cadence.
4. **`AiPlayerbot.IterationsPerTick`** — bounds action evaluation work per AI update.
5. **`AiPlayerbot.AsyncBotLogin`** — can move expensive login/randomization work away from the world thread, reducing spikes.
6. **Online population** — the direct linear lever when latency remains unacceptable.

`AiPlayerbot.RandomBotUpdateInterval` governs manager-level random-bot updates; it is not a substitute for measuring each bot's AI cadence.

## Capacity measurement procedure

1. Record CPU model/allocation, memory, co-tenants, source/image digest, map data, and all PlayerBots timing/activity settings in the private deployment record.
2. Establish an idle baseline with no players and a stable online-bot count.
3. Measure world CPU, resident memory, tick/perf reports, and restart count for a fixed interval.
4. Repeat with one real player near bots, then with a representative combat or dungeon workload.
5. Increase online bots in small steps. Change only one timing/activity lever between runs.
6. Stop before sustained CPU saturation, memory pressure, growing tick latency, or degradation of co-tenants.
7. Re-run after source, image, map, hardware, or major strategy changes.

## Reading the performance log (`perf.log`)

The world monitor writes `Update single map <id> inst <n>` and `Update map system` lines **only when an update exceeds `PerformanceLog.SlowMapUpdate` (default 200 ms)** — absence of lines is not proof of health, and any average computed from the log is worst-case-biased.

Per-map breakdown fields (single-map lines):

- `sess` — session processing; `players` / `players2` — the two player-update passes (PlayerBots AI and movement live here and dominate with large bot populations); `cells` — grid/cell updates (single-threaded on continents by default via `MapUpdate.Continents.MTCells.Threads`, while instanced maps get `MapUpdate.Instanced.UpdateThreads`); `sendObjUpdates` — object packet building; `relocations` — movement relocation; `wait N <ms>` — time this map's thread blocked on the map-system barrier.

`Update map system` totals the barrier across maps: the world loop paces at the **slowest** map, so per-continent work does not overlap past the boundary. A `wait` of seconds between maps means the system tick is dominated by one overloaded continent.

Ramp-up is not steady state: with sync login (`AsyncBotLogin = 0`) logins load characters, grids, and map tiles on the world thread, so mass login inflates ticks for minutes. Measure settled state only after `Login Character` lines in `char.log` stop growing, and remember that every restart replays the ramp when `RandomBotLoginAtStartup`/`RandomBotAutologin` are enabled.

## Empirical capacity notes (single deployment, mixed levels)

- With always-active mode, settled world-tick cost scaled roughly linearly with online bots (~1 ms per bot per map tick on the observed deployment): 50 bots ≈ 27 ms, 1,000 ≈ 0.5 s, 2,000 ≈ 1–3.4 s ticks. Treat these as order-of-magnitude anchors, not a portable ceiling — see the measurement procedure above.
- Ticks of 200–300 ms play like a ~250 ms-ping server: usable for solo PvE (questing, grinding, bot parties), not for reactive PvP. The 50 ms `MapUpdateInterval` budget is the ideal, not the achievable norm at scale.
- `RandomBotUpdateInterval` is manager-level (pool changes, teleports), **not** per-bot AI cadence; per-bot pacing is `ReactDelay` / `PassiveDelay` / `IterationsPerTick`.
- `AsyncBotLogin = 1` is documented as moving login off the world thread, but on at least one live image it wedged logins in an endless retry loop (see [ops gotchas](/ops/gotchas.md)); verify it on your image with a small population before relying on it at scale.

## Instrumentation

- Core world monitor: `.perf enable on`, `.perf intervalreport <seconds>`, `.perf cpu|memory|resources`.
- PlayerBots monitor: `AiPlayerbot.PerfMonEnabled` and the `.perfmon` chat command; output groups trigger (`T`), value (`V`), action (`A`), random-bot, and total metrics.
- Console `stats <guid>` reports the bot census and class/race/level/faction distribution.

Completion: the selected population is justified by reproducible measurements from the target deployment, not a copied universal ceiling.
