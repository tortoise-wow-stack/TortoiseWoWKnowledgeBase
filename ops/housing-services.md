---
type: Reference
title: Housing & character services
description: Guild housing (teleport bookmarks), shop-token character services (rename/race/appearance), and the variable/worldstate persistence.
tags: ["ops", "housing", "services"]
resource: mariadb://tw_char/guild_house
status: stable
generated: { by: pi/agent, at: 2026-08-11T16:45:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [Admin recipes via DB](/ops/admin-recipes.md) · [GM command cheat-sheet](/tuning/gm-commands.md) · [External integrations](/integrations/external-systems.md)

## Guild housing (no player housing)

A guild house is a **teleport bookmark**, not an instance: the guild master runs `.guild house on` at a location, which is saved to character-DB `guild_house` (`guild_id` primary key, `map_id`, `position_x/y/z`, `orientation`). Members teleport through the guild-house item's `spell_item_guild_house_teleport` script. `.guild house off` clears it and `.reload housing` reloads it. `SPELL_EFFECT_CREATE_HOUSE` (81) is unused. Query the target database for actual houses.

## Character services (shop tokens — item use scripts + commands)

| Token | Mechanism |
| --- | --- |
| 50000 Name Change | `item_character_rename` script: sets `AT_LOGIN_RENAME`, kicks player → client renames at login → `UPDATE characters SET name=..., at_login = at_login & ~AT_LOGIN_RENAME` |
| 80499 Guild Name Change | `.guild name "<new>"` — guild master + has item 80499 → `guild->Rename()` + consumes item |
| 80699 Appearance Change | `.copy <name>` — has item 80699, copies appearance/race/gender from another character |
| 50603–50613 Race Change | `shop_racechange` script: class checks, sets race + hardcoded bytes → `Player::ChangeRace()` + consumes item |

**Race change** (`Player::ChangeRace`) is the heaviest path: blocks guild leaders on faction change, leaves group, writes pdump backup `racechange_<guid>` (needs the pdump dir to exist!), re-maps skills/reps/quests/items/spells, logs to `racechange.log`. A free race token is mailed to players missing one (`HandleRaceChangeFixup`).

**GM rename:** `.rename` (rank 2) — no args = force rename at login (sets AT_LOGIN_RENAME); with name = direct UPDATE + cache refresh; "cancel" clears the flag. `.guild rename` / `.pet rename` = rank 3.

## `variable` & worldstates

`.variable <index> [value]` (rank 4) reads/writes a persistent uint32 in character-DB `variables` (`index`, `value`); known families include war-effort/Silithus state, Naxxramas attack count, and event flags. `.reload variables` refreshes it. `worldstates` is vestigial in this fork according to source TODOs; `saved_variables` holds legacy honor-maintenance markers. Query the target database for current rows.
