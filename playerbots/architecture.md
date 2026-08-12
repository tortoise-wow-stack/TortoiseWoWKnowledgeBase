---
type: Reference
title: PlayerBots architecture
description: Module layout, core classes, AI tick, strategy/action/trigger system, persistence.
tags: ["playerbots", "architecture"]
resource: https://github.com/Shyalya/tortoise-wow/tree/playerbots-integration-gh/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-11T15:30:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---
**Related:** [PlayerBots behavior systems](/playerbots/behavior-systems.md) · [PlayerBots modification](/playerbots/modification.md)

## §21 — PlayerBots deep dive: architecture

**Module layout:** flat root (framework) + `strategy/` tree: `actions/` (299 leaf behaviors), `triggers/` (48 conditions), `values/` (195 computed facts), `generic/` (113 cross-class strategies), per-class dirs (8–11 each), `tests/`. Root: PlayerbotAI, PlayerbotMgr, PlayerbotHolder, RandomPlayerbotMgr, TravelMgr/TravelNode (travel graph), PlayerbotFactory (bot char/gear gen), PlayerbotDbStore, PlayerbotSecurity, PlayerbotLoginMgr (async login), PlayerbotTextMgr, PerformanceMonitor/MemoryMonitor/BotLog, ChatFilter/Helper, AiFactory (engine assembly), scripts/ (offline bot_events.csv analysis).

**Ownership:** Player → (m_playerbotAI if bot | m_playerbotMgr if master) → holders own bot Players → each bot Player owns a PlayerbotAI → owns 4 Engines (BotState: combat/non-combat/dead/reaction) + AiObjectContext (name→object factory) → engines own strategies/triggers/multipliers; context owns actions/triggers/values by name.

**The tick:** core `Player::Update` → `PlayerbotAI::UpdateAI` → throttled by `aiInternalUpdateDelay` and the configured `ReactDelay`; idle minimal ticks use configured `PassiveDelay` and movement-only work → `UpdateAIInternal` drains chat replies and feeds packet queues through `ExternalEventHelper` opcode-to-trigger mapping → `DoNextAction` → `Engine::DoNextAction`: process triggers, push default actions, pop the highest-relevance basket, test usefulness, apply multipliers and prerequisites, test possibility, then execute. `IterationsPerTick` bounds work and is reduced in minimal mode. Strategy runtime uses `+name` add, `-name` remove, and `~name` toggle; combat state switches through combat-start/end/death events.

**Values:** `Value<T>` lazily cached facts (`AI_VALUE(T, "name")`), recomputed at most every checkInterval/2; ~195 concrete (health %, distance, targets, quest maps…). AiObjectContext::Update was DISABLED (was an 8% CPU no-op).

**Master:** SetMaster + guid-shadow revalidated every tick; free bots adopt group leader/nearby real player ("hello_follow"); masters removed when the group dissolves. Follow distance 1.5; bots mirror master's walk/sit; XP bonus via XpGainAction; quest share via CMSG_PUSHQUESTTOPARTY.

**Persistence:** bot state mostly runtime; module tables — chars DB: `ai_playerbot_random_bots`, `ai_playerbot_db_store` (k/v blob), `ai_playerbot_custom_strategy`, `ai_playerbot_names`, `ai_playerbot_cache`, `ai_playerbot_ahbot`; world DB: `ai_playerbot_travelnode(_link/path)` (travel graph), `ai_playerbot_named_location`, `ai_playerbot_zone_level`, `ai_playerbot_weightscales`, `ai_playerbot_enchants`, `ai_playerbot_equip_cache`, `ai_playerbot_*_cache`, `ai_playerbot_tele_cache`, `ai_playerbot_texts(_chance)`, `ai_playerbot_help_texts`, `ai_playerbot_guild_names`, `ai_playerbot_arena_team_names`, `ai_playerbot_rpg_races`.

**Performance scaling:** per-bot tick cost is approximately linear in active trigger/action evaluation. Guards include reaction-delay throttling, minimal-mode `PassiveDelay`, value/trigger check-interval caching, random-bot manager cadence with login throttling, slower battleground/LFG checks, activity scaling for bots far from players, and destination partitioning. Exact timing values are configuration/image facts; see [performance](/playerbots/performance.md).
