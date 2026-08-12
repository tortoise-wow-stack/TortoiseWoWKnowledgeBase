---
type: Reference
title: Battlegrounds & PvP
description: Supported battlegrounds (incl. custom Blood Ring and Sunnyglade), BG config keys, .bg GM commands, PvP settings — arena is NOT implemented.
tags: ["tuning", "pvp", "battlegrounds"]
resource: file:///opt/turtle/etc/mangosd.conf
status: stable
generated: { by: pi/agent, at: 2026-08-11T17:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [Server rates & limits](/tuning/rates-limits.md) · [PlayerBots behavior systems](/playerbots/behavior-systems.md) · [Config families](/tuning/config-families.md)

## Supported battlegrounds

`BattleGroundTypeId` (code in `src/game/Battlegrounds/`): **AV**=1 (map 30), **WS**=2 (map 489), **AB**=3 (map 529), **BR**=4 (map 26 — "Blood Ring", custom arena-style BG, auto-ports invitees after 1 s), **SV**=5 (map 27 — "Sunnyglade Valley", Turtle custom BG, `battleground_sunnyglade.cpp`). Brackets are hardcoded (10-level ranges) — **no max-level/start-delay config keys**. `IsArena()` = only BR; no teams/ratings.

## BG config keys

The audited source/image exposes `Battleground.CastDeserter`, queue announcer toggles, queue limits, invitation policy, premature-finish timing, premade waiting/group-size controls, queue randomization, battleground tagging, Alterac player thresholds, and per-battleground honor/reputation rates. Exact defaults and deployment overrides must be read from the pinned `.conf.dist` and private rendered config rather than copied from a live snapshot.

## Bots in BGs

`AiPlayerbot.RandomBotJoinBG = 1` (bots queue when idle, 30 s tick, level ≥ 10), `RandomBotAutoJoinBG = 0`. Bot bracket fill covers AV/WS/AB (+BR queue). Bots have full BG tactics strategies (flag carry in WSG/AV, objective moves — see playerbots behavior).

## GM commands (.bg — no .arena exists)

`.bg status` (list running BGs + queues), `.bg start` / `.bg stop` (must be INSIDE the BG; start only zeroes the delay — no forcestart-from-outside), bare `.bg` (per-BG debug commands).

## Arena — NOT implemented

No ArenaTeam code, no arena_team*tables, no Arena.* config keys. The only "arena" is the Blood Ring BG. `ai_playerbot_arena_team_names` and `RandomBotArenaTeamCount` are dead config (guarded by `#ifndef MANGOSBOT_ZERO`; this fork builds MANGOSBOT_ZERO).

## `PvP.*`

The fork exposes accurate equipment/purchase/timeline/reward gates, dishonorable-kill policy, open-world honor multiplier, Silithus and Eastern Plaguelands outdoor-PvP toggles, faction balance, and honor-cap/start settings. Treat values as deployment configuration: inspect the pinned default and current private override before changing them.
