---
type: Reference
title: Conditions, area triggers & teleports
description: The conditions system (64 enum members), area-trigger teleports, and named teleport locations.
tags: ["content", "conditions", "teleports"]
resource: mariadb://tw_world/conditions
status: stable
generated: { by: pi/agent, at: 2026-08-11T16:30:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [Quests](/content-creation/quests.md) · [NPCs](/content-creation/npcs.md) · [Conditional gossip and quest credit](/content-creation/gossip-quests.md) · [Items & GameObjects](/content-creation/items-gameobjects.md)

## Conditions (`conditions` in the world database)

Schema: `condition_entry` (PK auto_increment), `type` tinyint, `value1..4` int, `flags` tinyint. Flags: `0x1` = reverse result, `0x2` = swap targets.

**64 enum members** (`ConditionType` in `src/game/Conditions.h`): logical combinators `-3 NOT`, `-2 OR`, `-1 AND`, `0 NONE`, plus 60 positive condition types (`1` through `60`) — notable: 1 AURA, 2 ITEM, 3 ITEM_EQUIPPED, 4 AREAID, 5 REPUTATION_RANK_MIN, 6 TEAM, 7 SKILL, 8 QUESTREWARDED, 9 QUESTTAKEN, 12 ACTIVE_GAME_EVENT, 14 RACE_CLASS, 15 LEVEL, 17 SPELL, 19 QUESTAVAILABLE, 20/21 NEARBY_CREATURE/GO, 22 QUEST_NONE, 23 ITEM_WITH_BANK, 24 CONTENT_PHASE, 27 GENDER, 33 MAP_ID, 51 PVP_RANK, 53 LOCAL_TIME, 60 STAND_STATE.

**Where conditions gate content** (`condition_id` columns): all 10 loot templates, `gossip_menu` + `gossip_menu_option`, `npc_vendor` + `npc_vendor_template`, 12 DB-script tables (creature_ai_events/scripts, creature_movement_scripts, creature_spells_scripts, event/gameobject/generic/gossip/quest_start/quest_end/spell_scripts), `areatrigger_teleport.required_condition`; quests use `quest_template.RequiredCondition` instead. Evaluated via `sObjectMgr.IsConditionSatisfied(...)`. Invalid rows in `conditions` are erased; loaders for gossip and several other consumers reset a missing `condition_id` reference to `0`, which removes its gate rather than failing closed.

Actual use and type distribution depend on the world dataset. Query the target database when a change depends on existing condition entries.

For gossip, a failing option condition omits that option for ordinary players, while GMs still see it with a marker. A menu can have several text rows; the qualifying row with the numerically highest `condition_id` wins, so identifiers act as precedence as well as references. The fork has quest-state conditions but no general per-objective-complete condition; see [Conditional gossip and quest credit](/content-creation/gossip-quests.md).

## Area triggers (`areatrigger_teleport` in the world database)

Columns: `id` (PK — must exist in the client's AreaTrigger.dbc; radius/zone come from the DBC), `name`, `message`, `required_level`, `required_condition`, `required_phase`, `target_map`, `target_position_x/y/z`, `target_orientation`.

Fired on `CMSG_AREATRIGGER` when the player is within 5.0f of the trigger zone. **To add a custom teleport:** INSERT a row with an existing AreaTrigger.dbc id + target coords → `.reload areatrigger_teleport`.

## `game_tele` in the world database

Columns: `id` (PK auto_increment), `position_x/y/z`, `orientation`, `map`, `name`. `name` is the key used by `.tele <name>` in-game. Add: `INSERT INTO game_tele (position_x, position_y, position_z, orientation, map, name) VALUES (...)` → `.reload game_tele`.
