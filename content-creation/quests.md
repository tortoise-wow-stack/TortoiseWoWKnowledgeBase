---
type: Reference
title: Quests
description: quest_template essentials, relations, DB scripts vs C++, XP, reloads.
tags: ["content", "quests"]
resource: mariadb://tw_world/quest_template
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
**Related:** [NPCs](/content-creation/npcs.md) · [Spells](/content-creation/spells.md) · [Conditional gossip and quest credit](/content-creation/gossip-quests.md)


## §15 — Content creation: Quests (verified)

**quest_template essentials** (mixed legacy naming, mangos-zero + Tortoise additions; NO `Repeatable` column — repeatable = SpecialFlags bit 0x001, daily = 0x004; NO `RewMoneyDifficulty`):

| Purpose | Columns |
| --- | --- |
| Identity | `entry`, `Method` (0=autocomplete, 2=normal) |
| Level/zone | `ZoneOrSort` (neg = sort), `MinLevel`, `MaxLevel`, `QuestLevel`, `Type` (0 normal, 1 elite, 41 PvP, 62 raid, 84 escort) |
| Restrictions | `RequiredClasses`/`RequiredRaces` (bitmasks), `RequiredSkill(Value)`, `RequiredCondition` (→ `conditions`), `RequiredMin/MaxRepFaction(Value)`, `RepObjectiveFaction/Value` |
| Flags | `QuestFlags` (0x2 party, 0x8 shareable, 0x400 auto-rewarded), `SpecialFlags` (0x1 repeatable, 0x2 exploration, 0x4 daily, 0x80 **hardcore-only**, 0x100 yearly) |
| Chain | `PrevQuestId`, `NextQuestId`, `ExclusiveGroup`, `NextQuestInChain` |
| Source | `SrcItemId(Count)`, `SrcSpell` |
| Text | `Title`, `Details`, `Objectives`, `OfferRewardText`, `RequestItemsText`, `EndText`, `ObjectiveText1-4` |
| Objectives | `ReqCreatureOrGOId1-4` (neg = gameobject) + `ReqCreatureOrGOCount1-4`; `ReqItemId1-4` + `ReqItemCount1-4`; `ReqSourceId1-4(Count)`; `ReqSpellCast1-4` |
| Rewards | `RewXP` (**must be set — 0 = 0 XP**), `RewOrReqMoney` (neg = cost), `RewMoneyMaxLevel`, `RewSpell(Cast)`, `RewItemId1-4(Count)`, `RewChoiceItemId1-6(Count)`, `RewRepFaction1-5(Value)`, `RewMailTemplateId/DelaySecs/Money` |
| POI | `PointMapId`, `PointX`, `PointY` (no quest_poi tables in this fork) |
| Scripts | `StartScript`, `CompleteScript` → `quest_start_scripts` / `quest_end_scripts` |

**XP:** `Quest::XPValue` — RewXP × decay (≤ q+25 = 100% … q+30+ = 10%) × `Rate.XP.Quest` (skipped for Slow&Steady; War Mode ×1.2). At max level → `RewMoneyMaxLevel` instead.

**Scripting: NO SmartAI in this fork (zero matches).** DB-only: `quest_start_scripts`/`quest_end_scripts` (SD2-style: id, delay, command, datalong…, x/y/z/o, condition_id — commands include summon/cast/move/emote/say, exploration/event credit command 7, and map-event command 61), `quest_greeting` (greeting text + emote), `quest_cast_objective` (per-objective spellcast filters), `conditions`. **C++ needed only for:** `script_name` AI, escorts/cutscenes, ScriptedMapEvents. A plain kill/collect quest is 100% DB.

Talk-to-NPC and quiz objectives may also use `gossip_menu_option.action_script_id` → `gossip_scripts`. Trace the objective entry before choosing among ordinary `TalkedToCreature`, DB-script kill credit, and exploration/event completion; see [Conditional gossip and quest credit](/content-creation/gossip-quests.md).

**Reload:** `.reload quest_template` (also loads GO-for-quests), plus `quest_start_scripts`, `quest_end_scripts`, `quest_greeting`, `creature_questrelation`, `creature_involvedrelation`, `gameobject_questrelation`, `gameobject_involvedrelation`, `areatrigger_involvedrelation`, `locales_quest`, `points_of_interest`.
