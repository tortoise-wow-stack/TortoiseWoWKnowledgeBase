---
type: Reference
title: Items & GameObjects
description: item_template and gameobject_template essentials, loot tables, reloads, workflows.
tags: ["content", "items"]
resource: mariadb://tw_world/item_template
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
**Related:** [NPCs](/content-creation/npcs.md) · [Quests](/content-creation/quests.md)


## §13 — Content creation: Items & GameObjects (verified live)

**Schema quirk:** mangos-zero style — **snake_case** columns (`display_id`, `quality`…); no WotLK columns (no `FlagsExtra`, no socket fields). Source of truth: `sql/create_databases.sql`.

**item_template — minimal working item:** `entry` (PK), `class` (2=weapon 4=armor 7=recipe 15=misc), `subclass`, `name`, `display_id` (**must reuse an existing ID — client resolves model+icon from its own ItemDisplayInfo.dbc; a new ID = invisible item; no server-side icon table**), `quality`, `flags`, `buy_price`/`sell_price`, `inventory_type`, `allowable_class`/`allowable_race` (-1 = all), `item_level`, `required_level`, `stackable`, `bonding` (0 none/1 BoP/2 BoE/3 BoU/4 quest).

**Stats/effects:** `stat_type1..10`/`stat_value1..10` (3=agi 4=str 5=int 6=spi 7=sta), `armor`, `res` fields, `delay`, `dmg_min1..5`/`dmg_max1..5`/`dmg_type1..5`, `spellid_1..5` + `spelltrigger_1..5` (**0=use 1=equip 2=proc 4=learn**), `spellcharges_1..5` (-1 infinite), `spellcooldown_1..5`, `random_property`, `set_id`, `max_durability`, `disenchant_id`, `max_count`, `container_slots`, `start_quest`, `script_name`. Example (6948): `class 15, display_id 6418, quality 1, flags 64`.

**gameobject_template (type 3 = chest — fork differs from Trinity!):** `data0` = lockId (Lock.dbc; 0 = unlocked), **`data1` = lootId → gameobject_loot_template.entry** (NOT data0!), `data2` = restock seconds, `data3` = consumable (1 = despawns after loot), `data4/5` = min/max opens, `data6` = eventId. Verified: Sunken Chest 32: data0=43, data1=32.

**gameobject spawns:** `guid` (AUTO_INCREMENT PK), `id`, `map`, `position_x/y/z`, `orientation`, `rotation0..3` (quaternion: 0,0,sin,cos), `spawntimesecsmin`/`spawntimesecsmax` (fork has TWO columns), `animprogress`, `state` (1 = active).

**Loot tables** (same shape everywhere): `entry`, `item`, `ChanceOrQuestChance` (100=always, negative=quest-drop only), `groupid` (0 = independent, >0 = one per group), `mincountOrRef` (negative = reference_loot_template), `maxcount`, `condition_id`. Tables: `creature_loot_template`, `gameobject_loot_template`, `reference_loot_template`, `item_loot_template`, `skinning/fishing/pickpocketing/disenchant_loot_template`.

**Reload:** `.reload item_template` ✓, `.reload gameobject` (spawns) ✓, `.reload gameobject_loot_template` ✓ — but **NO `.reload gameobject_template`** (new GO templates need a server restart).

**Minimal workflow:** item_template → `.reload item_template` → test `.additem <entry>`; then GO template → GO spawn → loot rows → reloads.
