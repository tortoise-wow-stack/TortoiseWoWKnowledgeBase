---
okf_version: "0.2"
---

# Tortoise WoW server — knowledge bundle (OKF v0.2)

Deployment-agnostic knowledge for running and modifying a solo Tortoise WoW server (Turtle 1.18.1 core + PlayerBots). Entry point: [agent guide](AGENTS.md). Trust is recorded per concept; runtime facts must come from an owner-supplied private deployment record and a fresh read-only check. The PlayerBots capability baseline is pinned to source commit `172ee948e591f8bf1b53ea6389e3102186339f6e`; start at [PlayerBots capability map](playerbots/capability-map.md).

## ops

* [Access & status](ops/access-status.md) - How to reach the VM and confirm the world server is alive.
* [Accounts & permissions](ops/accounts.md) - Accounts, security levels (rank 0-6), how GM rights apply and refresh.
* [Admin recipes via DB](ops/admin-recipes.md) - Verified SQL: who is online, kick, password reset, gold, mail items, delete characters.
* [Server console & server control](ops/console.md) - Console command set, pending_commands DB queue, server shutdown/restart.
* [Everyday tasks](ops/everyday-tasks.md) - Verbatim commands for restart, logs, console, coins, bot count, backup.
* [Operational gotchas](ops/gotchas.md) - Client build gate, local image, DNS override, benign noise, volume pairs, handoff.
* [Housing & character services](ops/housing-services.md) - Guild housing (teleport bookmarks), shop-token character services (rename/race/appearance), and the variable/worldstate persistence.
* [Logs, monitoring & recovery](ops/logs-monitoring.md) - Log files and levels, .perf, crash recovery, AutoRestart, db-init migrations, disk growth.
* [Persistence map](ops/persistence.md) - Which config edits survive container recreates, ranked, with caveats.
* [Hot-reload commands](ops/reloads.md) - The full .reload table list — what can change without a restart.
* [Reference topology](ops/topology.md) - Deployment-neutral Compose services, data boundaries, network exposure, and storage preflight.

## tuning

* [Battlegrounds & PvP](tuning/battlegrounds-pvp.md) - Supported battlegrounds (incl. custom Blood Ring and Sunnyglade), BG config keys, .bg GM commands, PvP settings — arena is NOT implemented.
* [Config families (the rest of mangosd.conf)](tuning/config-families.md) - The config families beyond rates: Progression, PvP, GM, Log, chat anti-spam, server/ops, combat, corpses, pets, mail, visibility — plus surprising non-default values.
* [Env-driven config](tuning/env-config.md) - The .env variables that override config keys at every container start.
* [GM command cheat-sheet](tuning/gm-commands.md) - In-game GM commands by purpose with security levels.
* [Server rates & limits](tuning/rates-limits.md) - All Rate.* multipliers, limits and solo-play systems in mangosd.conf.
* [Server rate tuning and validation](tuning/rate-tuning-guide.md) - How to change XP, rewards, combat, skills, and related rate families while validating interactions and persistence.
* [Skills & talents data map](tuning/skills-talents.md) - What lives in DB (spell_template, skill_line_ability) vs DBC (talents).
* [Turtle systems](tuning/turtle-systems.md) - Challenges (Hardcore/War Mode/...), Glyphs, LFT, Transmog, AutoDonation, world buffs.

## playerbots

* [PlayerBots capability map](playerbots/capability-map.md) - Source-pinned public/user-operable surface map and progressive routing.
* [PlayerBots architecture](playerbots/architecture.md) - Module layout, core classes, AI tick, strategy/action/trigger system, persistence.
* [PlayerBots behavior systems](playerbots/behavior-systems.md) - Travel, questing, combat, professions, economy, social, PvP, groups, leveling, cheats.
* [PlayerBots command reference](playerbots/commands.md) - Router to exact `.bot`/`.rndbot`, chat, filter, action, transport, security, and lifecycle docs.
* [PlayerBots `.bot` / `.rndbot` commands](playerbots/console-commands.md) - Exact command aliases, parameters, targets, and important outputs.
* [PlayerBots chat and audience filters](playerbots/chat-surface.md) - Trigger parsing, channels, timing, and `@` audience selection.
* [PlayerBots actions, strategies, and state queries](playerbots/actions-strategies.md) - Build-conditional registries and addon-facing query formats.
* [PlayerBots addon transport](playerbots/addon-transport.md) - `debug`, raw addon responses, `#a`, and optional TCP framing.
* [PlayerBots security and failures](playerbots/security-failures.md) - Ownership gates and exact failure strings.
* [PlayerBots community documentation (ike3 line)](playerbots/community-docs.md) - The canonical ike3 mangosbot docs, community settings for solo servers, known issues, and the cmangos-fork feature diff.
* [PlayerBots config](playerbots/config.md) - aiplayerbot.conf inventory: population, behavior, premade specs, AhBot.
* [Bot creation pipeline & random-bot pool](playerbots/factory-pool.md) - How bots are created (Randomize phases, race/class/name/gear/professions/talents) and the random-bot pool lifecycle (events, teleports, re-randomize).
* [PlayerBots in-game usage](playerbots/in-game-usage.md) - How to command bots in-game: .bot, chat triggers, strategies, groups.
* [PlayerBots LLM & chat systems](playerbots/llm-chat.md) - The bot chat pipeline — scripted texts, broadcasts, speak/talk/say commands — and the LLM roleplay integration (plumbed but stubbed at the network layer).
* [PlayerBots modification](playerbots/modification.md) - Config keys inventory, SQL tables, custom strategy/action pattern, texts, travel data.
* [PlayerBots performance & capacity](playerbots/performance.md) - Source-derived cost model, high-impact levers, and a deployment-neutral capacity measurement procedure.

## content-creation

* [Conditions, area triggers & teleports](content-creation/conditions-areatriggers.md) - The conditions system (64 enum members), areatrigger_teleport, and game_tele locations — how content gating works in this fork.
* [DB migrations & SQL workflow](content-creation/db-migrations.md) - How SQL changes are shipped in this repack — migration files, the SHA1 tracking table, the boot-time auto-updater, and the manual sql/tools scripts.
* [World events & dynamic systems](content-creation/events-world.md) - game_event tables, world buffs, dynamic respawn, weather, periodic systems.
* [Factions, reputation & professions](content-creation/factions-professions.md) - DB-driven factions, rep rates, skill_line_ability, crafting flow, reloads.
* [Instances & bosses](content-creation/instances-bosses.md) - map_template, C++ boss mechanics, locks/resets, loot, AutoScaler, LFT.
* [Items & GameObjects](content-creation/items-gameobjects.md) - item_template and gameobject_template essentials, loot tables, reloads, workflows.
* [NPCs](content-creation/npcs.md) - creature_template, spawns, vendors, trainers, gossip, EventAI, reloads.
* [Quests](content-creation/quests.md) - quest_template essentials, relations, DB scripts vs C++, XP, reloads.
* [Spells](content-creation/spells.md) - spell_template columns, validation, client-side needs, no reload (restart).

## client-side

* [Client-side content (DBC/MPQ)](client-side/dbc-mpq.md) - Which client DBCs gate content, patch MPQ rules, tools, addons, Config.wtf.

## history

* [Project history & design decisions](history/implementation-plan.md) - What this project is, where it came from, and why the deployment record is kept outside this shareable bundle.

## references

* [Codebase map (source tree)](references/codebase-map.md) - Where everything lives in the Tortoise WoW source — src layout, script registration, module structure, sql and tools directories.
* [Community findings](references/community-findings.md) - Web research: lineage, fork history, solo-play advice, gotchas from the community.
* [Fork fix history & ecosystem](references/fix-history.md) - What the forks have already fixed (playerbots, class/spell, content), who maintains what, and the spell_mod technique for client-matching fixes.
* [Upstream resources (link index)](references/upstream-resources.md) - Every authoritative URL for this ecosystem — docs, forks, tools, wikis — in one place.

## integrations

* [External integrations (API, Discord, shop, shellcoins)](integrations/external-systems.md) - The HTTP transfer API, Discord bot, donation-shop flow, shellcoin economy, pending_commands producer and 2FA — how external systems hook into the core.
* [Turtle addon protocols (TW_ messages)](integrations/turtle-addon-protocols.md) - The addon-message surface the client addons use to talk to the server — LFG, shop, guild bank, transmog, titles and more.

## workflows

* [Change workflow (the golden path)](workflows/change-playbook.md) - Decision tree for making any change — config, SQL, C++, or client DBC — with the verify loop for each.
