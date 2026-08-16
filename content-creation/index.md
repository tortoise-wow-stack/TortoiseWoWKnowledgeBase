# content-creation — index

* [Conditions, area triggers & teleports](conditions-areatriggers.md) - The conditions system (64 enum members), areatrigger_teleport, and game_tele locations — how content gating works in this fork.
* [DB migrations & SQL workflow](db-migrations.md) - How SQL changes are shipped in this repack — migration files, the SHA1 tracking table, the boot-time auto-updater, and the manual sql/tools scripts.
* [World events & dynamic systems](events-world.md) - game_event tables, world buffs, dynamic respawn, weather, periodic systems.
* [Factions, reputation & professions](factions-professions.md) - DB-driven factions, rep rates, skill_line_ability, crafting flow, reloads.
* [Conditional gossip and quest credit](gossip-quests.md) - How menu text, options, conditions, branches, DB scripts, and quest-objective credit fit together.
* [Instances & bosses](instances-bosses.md) - map_template, C++ boss mechanics, locks/resets, loot, AutoScaler, LFT.
* [Items & GameObjects](items-gameobjects.md) - item_template and gameobject_template essentials, loot tables, reloads, workflows.
* [NPCs](npcs.md) - creature_template, spawns, vendors, trainers, gossip, EventAI, reloads.
* [Quests](quests.md) - quest_template essentials, relations, DB scripts vs C++, XP, reloads.
* [Spells](spells.md) - spell_template columns, validation, client-side needs, no reload (restart).
