---
type: Reference
title: World events & dynamic systems
description: game_event tables, world buffs, dynamic respawn, weather, periodic systems.
tags: ["content", "events"]
resource: mariadb://tw_world/game_event
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
**Related:** [Instances & bosses](/content-creation/instances-bosses.md) · [Turtle systems](/tuning/turtle-systems.md)

## §17 — World events & dynamic systems (verified)

**game_event tables:** `game_event` (entry, start_time, end_time, **occurence = minutes between occurrences**, **length = duration minutes**, holiday, description, hardcoded, disabled, required_phase), `game_event_creature` (guid, event; negative = despawn during event), `game_event_creature_data` (model/equipment/spells swap), `game_event_gameobject` (neg = despawn), `game_event_mail` (neg = send at stop), `game_event_quest`. Active events persist in character-DB `game_event_status` and resume across restarts. GM: `.event list|start|stop|enable|disable`, `.lookup event`. No `game_event_npcflag`, `game_event_condition`, or `game_event_pool` exists in this fork. Query the target world dataset for its actual event inventory.

**AutoWorldBuff** (fork, `Enable = 0`): per-buff independent timers (random min/max 1–3 h, warning at `WarningInterval`), casts on real players only (no bots): Spirit of Zandalar (24425, STV), Warchief's Blessing (16609, Horde — Crossroads/Org), Rallying Cry of the Dragonslayer (22888, capitals).

**Dynamic respawn:** `DynamicRespawn.Range = 120`, `PercentPerPlayer = 7`, `MaxReductionRate = 0.25`, `MinRespawnTime = 25` (elite/indoor variants), bounds `AffectRespawnTimeBelow = 900`, `AffectLevelBelow = 60`, `PlayersThreshold = 4` — continents only, reduces respawn time with player count nearby.

**Weather:** `game_weather` (zone + per-season rain/snow/storm chances 0–100), re-rolled every 10 min; `.weather` GM command.

**Zone control: none** (no territory system; only the hardcoded Silithus PvP event).

**Periodic systems** (World::Update): auctions 1 min, `pending_commands` 1 min, save vars 1 min, uptime 10 min, shellcoin 10 min, corpses 20 min, census 60 min, total money 6 h, groups 1 s, events dynamic; every tick: LFT/LFG/BG/transport/guard/zone scripts, dynamic visibility, **playerbots tick**, autobroadcast (60 s), guild/daily-quest managers, mass mail. Player autosave 15 min (`.saveall` available). AutoDonationPoints (Enable=0): shop coins for online time, 1 h interval, persisted in `donation_point_progress`. **No AuctionHouseBot** (AhBot replaces it, §2).
