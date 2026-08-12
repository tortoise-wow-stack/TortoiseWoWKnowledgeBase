---
type: Reference
title: Codebase map (source tree)
description: Where everything lives in the Tortoise WoW source — src layout, script registration, module structure, sql and tools directories.
tags: ["references", "codebase"]
resource: https://github.com/Shyalya/tortoise-wow
status: stable
generated: { by: pi/agent, at: 2026-08-11T18:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

# Codebase map (source tree)

**Related:** [Change workflow](/workflows/change-playbook.md) · [PlayerBots architecture](/playerbots/architecture.md) · [Instances & bosses](/content-creation/instances-bosses.md)

## src/

- `src/game/` — the world server core: AccountMgr, AI, Anticheat, AuctionHouse, **Autoscaling** (AutoScaler), **Battlegrounds** (AV/WS/AB/BR/SV), Chat (command tables!), Commands (command handlers), Conditions, **LFT** (custom dungeon finder), Maps, Objects, **Shop** (donation shop), Spells (SpellMgr, SpellEffects), TransmogMgr, World (config load, update loop), Handlers (opcodes), Database (DBCStores, SQLStorages), HttpApi (transfer API), DiscordBot.
- `src/scripts/` — content scripts: `dungeons/` (38 dungeon dirs, `instance_*.cpp` + `boss_*.cpp`), `battlegrounds/` (incl. `battleground_sunnyglade.cpp`), `spells/` (`spells_turtle.cpp`, class spell scripts), `events/`, `miscellaneous/` (feature_transmog, glyph_master, shop_racechange, random_scripts_1.cpp), `world/`. **Registration**: every script does `new Script; Name="..."; RegisterSelf()` and is declared in `ScriptLoader.cpp` — adding a script file means adding it to the build and ScriptLoader.
- `src/mangosd/` — the server binary: CliRunnable (console/FIFO), Master, WorldRunnable.
- `src/realmd/` — auth server: AuthSocket (SRP6, version gate), RealmList (accepted builds table), pending_commands consumer is in World (game), not here.
- `src/modules/PlayerBots/` — the bot module (see playerbots group); built with `-DBUILD_PLAYERBOTS=ON`; its SQL lives in `src/modules/PlayerBots/sql/{characters,world}`.
- `src/shared/` — framework: Log, Config, httplib.h, HttpApi, DiscordBot, Database.
- `src/framework/` — low-level shared code.

## sql/

- `create_databases.sql` — full schema (single source of truth for DDL).
- `sql/base/` — 186 files of world data (131 MB) — the world DB ships in the repo; only client data (dbc/maps/vmaps/mmaps) must be extracted from a client.
- `sql/database_updates/` — 130 timestamped migrations (`<yyyymmddhhmmss>_<realm>.sql`) applied by the auto-updater at boot; tracked by SHA1 in `tw_world.migrations`.
- `sql/logon/` — logon DB extras (e.g. `donation_point_progress.sql`).
- `sql/tools/` — manual one-off scripts: `tool_easy_recipes.sql`, `druid_forms_backfill.sql`, `graveyards_turtle_dungeons.sql` (needs `tools/dbc/add_worldsafelocs.py` first), `playerbot_bypass_crossroads.sql` (travel-graph link rewrite — check your node ids), `char_fix_guild_bank_tabs.sql`, `penqle_guid_remap.md`, `realm_specific_*.sql`, `tool_*.sql` helpers.

## tools/

`BuildEverything.bat`, `CinematicTool`, `DiscordOverlay`, `TurtlePatcher` (client patcher), `extractor/`, `vmap_extractor/`, `vmap_assembler/`, `mmap/` (MoveMapGen + `mmap_extract.py`), `model_reader`, `port`, `RealmMerge`, `TGAtoPNG`, `dbc/` (incl. `add_worldsafelocs.py`), `talents/` (`build_premade_specs.py`), `checkegglogs`.

## Config sources

- `src/mangosd/mangosd.conf.dist.in` — mangosd.conf template (incl. the fork additions block, ~lines 2023–2237).
- `src/modules/PlayerBots/playerbot/aiplayerbot.conf.dist.in` — bot config template (3644 keys).
- `src/realmd/realmd.conf.dist.in`, `src/game/Shop/`, `src/game/LFT/` — subsystems.
