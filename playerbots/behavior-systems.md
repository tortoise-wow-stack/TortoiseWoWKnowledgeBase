---
type: Reference
title: PlayerBots behavior systems
description: Travel, questing, combat, professions, economy, social, PvP, groups, leveling, cheats.
tags: ["playerbots", "behavior"]
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
**Related:** [PlayerBots command reference](/playerbots/commands.md) · [PlayerBots architecture](/playerbots/architecture.md)


## §24 — PlayerBots: behavior systems (what bots can do)

Every behavior = a **strategy** (strategy/generic/*.cpp) registering TriggerNode→NextAction pairs; class rotations in strategy/{class}/; AiFactory composes defaults per class/spec/role.

**Travel:** TravelMgr singleton + per-bot TravelTarget (destinations: QuestGiver/QuestObjective/Vendor/AH/Repair/Mail/Trainer/Grind/GatherX/Boss/Explore/Rpg); node graph with A* (link types: walk, areaTrigger, transport, **flightPath/taxi**, teleportSpell/portal, staticPortal); data in `ai_playerbot_travelnode(_link/_path)` — auto-generated at runtime if empty (needs maps/vmaps/mmaps); `ai_playerbot_named_location` for named spots. Random bots teleport on schedule (RandomBotTeleportMin/MaxInterval 1–7 days) to level-appropriate zones, optionally clustering near players.

**Questing:** "quest" strategy — talk to giver, travel to objective, grind, turn in; `AutoDoQuests` gates the travel strategy; `SyncQuestWithPlayer` = bots copy the master's quests and loot quest items for you; RPG variant ("rpg quest"); random bots get class chains + `RandomBotQuestIds` at creation; `BotCheats=quest` = auto-complete.

**Combat:** target selection, threat management (`ThreatMultiplier` — AOE threat ≥50 suppressed, taunt/stop at high), pulling (ranged pull), fleeing/kiting (`FleeManager`), CC (per-class), avoid-AOE, trinket/lightwell timers, unstuck; roles from class+spec (BOT_ROLE_TANK/HEALER/DPS via GetPlayerRoles): tank = "tank assist"+"pull", healer = party-heal/dispel/resurrect values (PartyMemberToHeal, LeastHpTargetValue), DPS = "dps assist"; dungeon/raid fight strategies (MoltenCore/BWL/Karazhan/Naxx/Onyxia — positioning, dispels, boss tactics); grinding via "attack anything" + Grind travel purpose.

**Professions:** chat `craft [itemId]` (finds recipe, collects reagents, crafts, trades with fee — `GetCraftFee`); guild craft orders (members order, bots with recipe craft); gathering = reveal nearby ore/herbs + travel to gather spots; bots get random professions/recipes at creation (PlayerbotFactory::InitTradeSkills) and visit trainers.

**Economy:** `ah`/`ah bid` chat words (price from per-item cache; one bot at a time); `sell`/`buy`/`repair`; BudgetValues drive vendoring (ShouldGetMoney); `BotCheats=gold` = free money.

**Social:** greetings (EnableGreet), broadcasts (EnableBroadcasts + per-channel chances: world/general/guild/trade/LFG…), combat callouts ("say::critical health" etc.), guilds (create/join/meetings via travel), custom::say DB strategies.

**PvP/BG:** `.rndbot` BG queue join (RandomBotJoinBG, joins only when real players queue unless AutoJoinBG), full BG tactics (move to objective, flag carry in WSG/AV, check flag), world-PvP attack, duels.

**Group/raid:** role→LFG slot mapping; invite nearby/guild; accept master's invite; LFT queue ("lfg join"); RTI kill-order marking (tank/dps assist attack the marked target).

**Leveling:** free bots get bonus XP (server rate × `XPRate` = 3); on level-up auto talents (premade spec) + auto-learn spells (AutoPickTalents full); incremental re-randomize (bags/spells/skills/talents/gear); gear upgrades in place when `RandomGearUpgradeEnabled`.

**Cheats** (`.bot cheat +x,-x` GM): taxi (free flight), gold, health, mana, power, item (craft without reagents), cooldown, repair (no durability loss), movespeed ×10, attackspeed, breath (water breathing), glyph (free), quest (auto-complete). Defaults: `BotCheats = repair,breath`, `RndBotCheats = repair,breath,item`.

**Special:** `.rndbot always <name>` = offline AI (a logged-out character keeps playing); `.bot prepare` = add consumables/reagents; `.bot init [white|green|blue|epic|legendary|sync]` = full re-randomize at a gear quality (sync = copy master).
