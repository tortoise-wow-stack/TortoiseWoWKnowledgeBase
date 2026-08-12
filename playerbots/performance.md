---
type: Reference
title: PlayerBots performance & capacity
description: Source-derived cost model, tuning levers, and a deployment-neutral measurement procedure.
tags: [playerbots, performance, capacity]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T12:00:00Z }
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

## Instrumentation

- Core world monitor: `.perf enable on`, `.perf intervalreport <seconds>`, `.perf cpu|memory|resources`.
- PlayerBots monitor: `AiPlayerbot.PerfMonEnabled` and the `.perfmon` chat command; output groups trigger (`T`), value (`V`), action (`A`), random-bot, and total metrics.
- Console `stats <guid>` reports the bot census and class/race/level/faction distribution.

Completion: the selected population is justified by reproducible measurements from the target deployment, not a copied universal ceiling.
