---
type: Reference
title: PlayerBots autonomy and limits
description: "Source-pinned overview of what random PlayerBots can do without a master, which settings activate those behaviors, and where the automation is unreliable."
tags: ["playerbots", "autonomy", "behavior"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-16T19:35:11Z }
verified: { by: process:source-audit, at: 2026-08-16T19:35:11Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---

**Related:** [PlayerBots architecture](architecture.md) · [behavior systems](behavior-systems.md) · [offline alts vs random bots](bot-lifecycle.md) · [config](config.md) · [known issues](community-docs.md)

## Short answer

Random or “free” PlayerBots can act without a human master. They can fight, travel, quest, loot, gather, craft, use vendors, repair, train, retrieve mail, use the auction house, join groups/LFG, speak scripted lines, and participate in battleground flows when the corresponding strategies and configuration are active.

They are not learning agents or human-level players. Their behavior is a large, hand-written rule system: triggers and cached game values select from prioritized actions, while strategy/configuration, money, inventory, map data, group state, and security gates decide whether an action is allowed. A capability in the source is therefore not a promise that every bot will perform it in every deployment.

## Which kind of bot?

| Bot mode | Who supplies the goal? | Autonomous world activity |
| --- | --- | --- |
| Owned/alt bot | A real player's `PlayerbotMgr` and commands | Usually follows the master and group state |
| Random/free bot | `RandomPlayerbotMgr` plus its strategy set | Can roam, level, socialize, and maintain itself without a master |
| `.bot always` offline alt | The random manager keeps an owned character's AI active | Separate from the random account pool; do not treat it as a random bot |

The lifecycle, ownership, login, and readiness differences are documented in [bot-lifecycle](bot-lifecycle.md). “Autonomous” below means the random/free path, not an owned bot waiting for commands.

## How the AI makes decisions

Each bot has separate combat, non-combat, reaction, and death behavior. On an AI update it evaluates state such as health, threat, inventory, durability, quests, distance, travel targets, money, and nearby units. Active strategies register triggers; a trigger proposes one or more actions; relevance, prerequisites, cooldowns, class/role rules, and safety checks filter the candidates before the bot executes one.

This is deterministic/stateful automation with random choices and priorities. It does not learn from previous play, invent a long-term plan, or understand arbitrary natural-language goals. The [architecture](architecture.md) page covers the tick and strategy/action model in detail.

## What a free bot can do

The table describes source capability. The “activation” column is the important caveat: a deployment can disable a strategy or change the conditions without changing the compiled source.

| Activity | Capability in the pinned source | Important activation or limit |
| --- | --- | --- |
| Combat | Class/spec rotations, target selection, threat control, healing, tanking, DPS assistance, interrupts, crowd control, fleeing, buffs, consumables, and encounter strategies | Class, role, combat strategy, group state, and spell/data correctness matter |
| Questing | Accept suitable quests, travel to quest givers/objectives, use quest actions, fight and loot, return to quest givers, turn quests in, and use a configurable reward mode | `AutoDoQuests` gates the random-bot travel/RPG path and defaults to enabled in the pinned source; quest sync is a separate feature |
| Grinding | Select grind travel targets and attack suitable enemies | Requires the grind strategy and valid level/zone data |
| Looting | Loot corpses and game objects, with quest, bag-space, group-loot, and item-usage checks | Loot rules and full bags can prevent an otherwise valid loot action |
| Gathering | Mine, herb, skin, fish, and travel to gathering targets | Requires gathering data, the relevant profession, and usable travel paths |
| Crafting | Learn/use trade skills, obtain reagents, craft useful or skill-up items, and participate in some guild craft flows | Recipe, reagent, skill, inventory, and strategy checks apply |
| Vendors | Buy useful ammunition, consumables, gear, reagents, and sell items classified for vendor use | It does not simply sell every item; item-usage, money, bag space, and nearby NPC checks gate the action |
| Repair and training | Travel to armorers/trainers, repair damaged equipment, and train available spells or skills | Maintenance strategy, durability, money, trainer data, and related automation settings apply |
| Mail | Travel to mailboxes and retrieve mail containing items or money, including auction-related mail | Delivery time, bag space, money needs, and mail strategy affect when it happens |
| Auction house | Travel to auctioneers, post items classified for AH use, bid/buy useful listings, and use auction mail | Price/item-usage evaluation, deposit money, free budget, bag space, and `rpg vendor` gates apply |
| Social and groups | Scripted speech, greetings, guild activity, duels, group invitations/acceptance, following, trading useful items, and LFG behavior | Ownership, group rules, range, security, and strategy state constrain interactions |
| Battlegrounds | Queue and use battleground strategies | `RandomBotJoinBG` enables the path; with `RandomBotAutoJoinBG` disabled, the queue generally needs real-player activity rather than an empty bot-only queue |
| Exploration and travel | Use walking, area triggers, transports, flight paths/taxis, portals/teleports, and named destinations such as cities, trainers, vendors, AH, mail, repair, grind, and quest objectives | Travel-node data and maps/vmaps/mmaps are prerequisites; cross-map movement is a known failure area |
| Leveling and upkeep | Gain XP, choose premade talents, learn/train configured spells, upgrade equipment, manage consumables, and periodically re-randomize parts of a random bot | Starting level, XP, gear, talent, training, and cheat settings are deployment choices |

The source implements the RPG quest and vendor strategies explicitly: [RpgStrategy.h](https://github.com/Shyalya/tortoise-wow/blob/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot/strategy/generic/RpgStrategy.h) describes quest-giver, vendor, AH, mailbox, repair, and trainer behavior, while [RpgStrategy.cpp](https://github.com/Shyalya/tortoise-wow/blob/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot/strategy/generic/RpgStrategy.cpp) registers the corresponding actions.

## Questing: yes, but not perfectly

Questing has two easily confused paths:

* The normal quest strategy handles quest shares, quest-giver interaction, completion, and related quest actions.
* The random/free-bot factory adds `travel`, `tfish`, and `rpg` when `AutoDoQuests` is enabled. The RPG quest strategy seeks NPCs with suitable quests, favors experience-giving quests, and also considers repeatable quests.

`SyncQuestWithPlayer` is different: it makes a bot mirror a player's quest flow when grouped. It is not required for a free bot to quest on its own. `PreQuests` is also different: it controls quest pre-completion during bot creation and should not be mistaken for gameplay questing.

Quest rewards can be automatic, listed for selection, or left for the player depending on the reward mode/configuration. Questing can still stall on missing travel data, unusual objectives, quest-item loot, group loot rules, reward handling, or a state that the strategy does not recognize. Expect autonomous progress, not a guaranteed perfect completion of every chain.

## Vendors, AH, and the economy

The PlayerBots module contains two distinct ideas that are often conflated:

1. **PlayerBot economy actions:** a bot can visit vendors, repairers, trainers, mailboxes, and auctioneers as part of its own RPG/maintenance behavior. It classifies items by use and checks budgets, bag space, deposit costs, and pending maintenance before buying, selling, or posting.
2. **A dedicated AH market-maker:** the separate `AhBot.*`/legacy `AuctionHouseBot.*` configuration families control synthetic auction-house population. Enabling or disabling that system is not the same as enabling a PlayerBot's ability to visit and use a normal auction house.

The exact source gates are in [MaintenanceValues.h](https://github.com/Shyalya/tortoise-wow/blob/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot/strategy/values/MaintenanceValues.h) and the AH actions in [AhAction.cpp](https://github.com/Shyalya/tortoise-wow/blob/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot/strategy/actions/AhAction.cpp). These are decision rules, not a promise that the AH will be populated or economically balanced.

## How “wild” autonomy works

The random manager maintains a configured population: it creates or selects characters, logs them in/out, schedules updates, changes strategies, handles death/revival bookkeeping, and may reposition or re-randomize bots. A free bot can therefore continue acting when no real player is nearby, subject to activity-priority and strategy settings.

Its autonomy is bounded in three ways:

* **Goals are supplied by strategies.** A random bot may grind, wander, quest, craft, or pursue maintenance because those strategies were installed; it does not decide that a new life goal would be useful.
* **Actions are conditional.** The bot may want to sell but lack a vendor target, want to AH an item but lack deposit money, or want to quest but lack a valid travel target.
* **The world model is incomplete.** Pathfinding, maps, group loot, quest scripts, unusual gossip, and encounter mechanics can defeat a valid strategy. Bots can wait, wander, retry, or need intervention.

The default factory composition is visible in [AiFactory.cpp](https://github.com/Shyalya/tortoise-wow/blob/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot/AiFactory.cpp). In particular, a random non-combat strategy list that does not literally contain `+quest` does not by itself prove that autonomous questing is disabled: the factory installs the base quest strategy and separately gates the travel/RPG additions with `AutoDoQuests`.

## Activation checklist

When investigating a specific deployment, check these independently rather than inferring behavior from the existence of an action in the catalog:

| Setting/data | What it answers |
| --- | --- |
| `AiPlayerbot.AutoDoQuests` | May the random/free path pursue quests and related travel/RPG behavior? |
| `AiPlayerbot.SyncQuestWithPlayer` | Should a bot mirror a player's quest flow? |
| `AiPlayerbot.RandomBotNonCombatStrategies` | Which random-bot non-combat behavior is selected after factory defaults? |
| `AiPlayerbot.RandomBotJoinLfg`, `RandomBotJoinBG`, `RandomBotAutoJoinBG` | May bots use LFG/BG paths, and may they seed a queue without real players? |
| `AiPlayerbot.AhBot.*` and `AuctionHouseBot.*` | Is the separate AH market-maker active? |
| `AiPlayerbot.BotCheats` and `RndBotCheats` | Are bots receiving repair, item, taxi, gold, or other assistance? |
| Travel tables and map/vmap/mmaps | Can the bot find and reach the intended destination? |
| Online population/activity scheduling | Is the bot actually being updated, or intentionally treated as idle? |

Runtime values belong in a private deployment record; this shareable bundle documents the source baseline and the checks needed to interpret a live result. See [config](config.md), [performance](performance.md), and [community findings](community-docs.md) for the detailed inventories and failure notes.

## How advanced are they?

| Dimension | Assessment |
| --- | --- |
| Breadth of game systems | High: the module reaches most ordinary PvE, travel, progression, profession, group, and economy surfaces |
| Ordinary PvE combat | Strong when class/role strategies and encounter data fit the situation |
| Unsupervised routine activity | Medium to high: random bots can maintain a loop of travel, combat, loot, upkeep, and social activity |
| Human-like reasoning | Low: no learning, world understanding, or open-ended planning |
| Edge-case reliability | Moderate to poor: unusual quests, terrain, data gaps, and complex mechanics can stall or mis-prioritize the bot |

The conversational layer does not change that assessment in this baseline. Scripted chat and broadcasts work, but `PlayerbotLLMInterface::Generate()` returns no response in the pinned source; the LLM path is plumbed but stubbed. See [LLM and chat systems](llm-chat.md) and [PlayerbotLLMInterface.cpp](https://github.com/Shyalya/tortoise-wow/blob/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot/PlayerbotLLMInterface.cpp).
