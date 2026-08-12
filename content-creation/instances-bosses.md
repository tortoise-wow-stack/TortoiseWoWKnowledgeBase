---
type: Reference
title: Instances & bosses
description: map_template, C++ boss mechanics, locks/resets, loot, AutoScaler, LFT.
tags: ["content", "instances", "bosses"]
resource: mariadb://tw_world/map_template
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
**Related:** [Quests](/content-creation/quests.md) · [Events & dynamic systems](/content-creation/events-world.md)

## §18 — Instances & bosses (verified)

**`map_template`** (renamed from `instance_template`): `entry, parent, map_type (1 = 5/10-man, 2 = raid), linked_zone, player_limit, reset_delay (days, × Rate.InstanceResetTime, minimum 1), time_offset, ghost_entrance_map/x/y, map_name, script_name`. There is no `allowMount` column; mount permission is hardcoded by map ID. Query the target world dataset for its instance inventory and reset values.

**Boss mechanics = C++ ONLY.** `map_template.script_name` → ScriptedInstance in `src/scripts/dungeons/<name>/` (38 dungeons, 35 instance_*.cpp, boss_*.cpp per boss). **No smart_scripts anywhere.** DB-driven alternative: legacy EventAI (`ai_name='EventAI'` + `creature_ai_events/scripts`). `script_name` also on creature_template/gameobject_template/spell_template/areatrigger — same dispatch.

**Boss rows:** `rank` enum: **0 normal, 1 elite, 2 rare-elite, 3 WORLD BOSS, 4 rare** (rank 3 is not ordinary elite here). `flags_extra` 0x1 = INSTANCE_BIND (raid bind on kill; there is no DUNGEON_BOSS flag). Source/content examples such as Ragnaros use a `boss_*` script name; query the pinned world dataset before relying on specific entries or counts.

**Locks/saves:** `character_instance` (guid, instance, permanent) per player; `group_instance` per group; `instance` (id, map, resettime, data — blob of InstanceData); `instance_reset` (global raid reset times). Permanent bind on INSTANCE_BIND kill. Reset engine: dungeons per-instance (max respawn + 2 h), raids global at `today + reset_delay*DAY + Instance.ResetTimeHour` (4 AM), warnings at 3600/900/300/60 s.

**Loot:** `groupid = 0` means independent rolls; `groupid > 0` means one roll per group; `mincountOrRef < 0` references `reference_loot_template`. Query the target world dataset for actual row counts and references.

**AutoScaler** (fork, `AutoScalerEnable = 0`): linear HP/damage scaling by playerCount/maxPlayers with per-size clamps (5/10/20/40-man), `GenerateScaledMoneyLoot`, opt-out table `disabled_dungeon_scaling`.

**Dungeon finder:** legacy LFGMgr (meeting stones) + custom **LFT** (addon-driven, `TW_LFG` guild-chat protocol, teleport via map_template entrances, bot fill via LFTBotFill, listings in `lft_user_groups`). `lfgdungeons` tables are vestigial (0 rows).

**To add/modify a boss:** mechanics = C++ in src/scripts/dungeons/ (+ `script_name` wiring); stats/loot/reset times = pure SQL.
