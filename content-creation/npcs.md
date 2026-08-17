---
type: Reference
title: NPCs
description: creature_template, spawns, vendors, trainers, gossip, EventAI, reloads.
tags: ["content", "npcs"]
resource: mariadb://tw_world/creature_template
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
**Related:** [Items & GameObjects](/content-creation/items-gameobjects.md) · [Quests](/content-creation/quests.md) · [Conditional gossip and quest credit](/content-creation/gossip-quests.md)

## §14 — Content creation: NPCs (verified live)

**creature_template — minimal set:** `entry`, `name`, `display_id1` (→ CreatureDisplayInfo.dbc; fork also has DB overrides `creaturedisplayinfo*`, `creature_display_info_addon`), `level_min/max`, `health_min/max`, **`faction` (THE column: hostile 25 / friendly 11)**, `npc_flags` bitmask (1=gossip, 2=questgiver, 128=vendor, 16=trainer; therefore 3=gossip+questgiver and 19=gossip+questgiver+trainer), `rank`, `dmg_min/max`, `unit_class`, `type` (7=humanoid), `loot_id`, `gold_min/max`, `equipment_id`, `ai_name` ('' = default; EventAI/GuardAI/NullAI/ReactorAI…), `movement_type` (0 idle/1 random+wander_distance/2 waypoint), `inhabit_type` (1 ground/3 ground+swim), `script_name` (C++ only). Defaults are safe — hostility is purely faction.

**creature (spawns):** `guid` (PK auto; unique per NPC, 0 = spawns everywhere), `id`, `id2/id3/id4` (extra copies), `map`, `position_x/y/z`, `orientation`, `spawntimesecsmin/max`, `wander_distance`, `health_percent`/`mana_percent` (not curhealth!), `movement_type` (spawn wins over template), `spawn_flags`. Waypoints: `creature_movement` (id = spawn guid, point, x/y/z, waittime, script_id).

**Vendor:** `npc_vendor` (entry, slot, item, maxcount/incrtime = limited stock, itemflags, condition_id) — or `npc_vendor_template` via `trainer_id`/`vendor_id` in template. A vendor-backed gossip option needs both the creature vendor flag (`npc_flags` bit 128) and a matching `gossip_menu_option.npc_option_npcflag`; item price is read from `item_template.buy_price`, while `npc_vendor.condition_id` is checked when listing and buying. **Trainer:** `npc_trainer` (entry, spell, spellcost, reqskill, reqskillvalue, reqlevel) or `npc_trainer_template`. **Quest giver/turn-in:** `creature_questrelation` / `creature_involvedrelation` (id, quest).

**Gossip (broadcast-text based — NO text0_0 columns!):** `creature_template.gossip_menu_id` → `gossip_menu` (entry, text_id, script_id, condition_id) → `npc_text` (ID, BroadcastTextID0-7, Probability0-7) → text lives in `broadcast_text`. Options: `gossip_menu_option` (menu_id, id, option_icon, option_text, option_broadcast_text, option_id, npc_option_npcflag, action_menu_id, action_poi_id, action_script_id, box_coded, box_money, box_text, condition_id).

For conditional options, multi-page dialogue, and talk/quiz objectives, continue with [Conditional gossip and quest credit](/content-creation/gossip-quests.md). In particular, page-level `script_id` and option-level `action_script_id` fire at different times, and quest credit is not implied by opening a response page.

**Equipment:** `creature_equip_template` (entry, equipentry1..3 = item DISPLAY ids, not item ids; 0 = bare hands). Per-spawn cosmetics: `creature_addon` (guid, mount, bytes1, sheath, emote, auras).

**EventAI** (spell-casting/scripted events, DB-only): `creature_ai_events` (creature_id, condition_id, event_type (4=on aggro…), event_chance, event_flags, event_param1-4, action1_script..3, comment) + `creature_ai_scripts` (id, delay, command, datalong1-4, target_type, dataint, x/y/z, condition_id).

**Reload:** `.reload creature_template [entry]`, `.reload creature`, `.reload npc_vendor`, `.reload npc_trainer`, `.reload creature_questrelation/involvedrelation`, `.reload gossip_menu/gossip_menu_option`, `.reload npc_gossip`, `.reload npc_text`, `.reload creature_ai_events`, `.reload creature_loot_template`, `.reload conditions`, `.reload all`. Movement/waypoints need respawn or restart.
