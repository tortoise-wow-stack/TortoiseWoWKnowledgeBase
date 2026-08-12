---
type: Reference
title: Skills & talents data map
description: What lives in DB (spell_template, skill_line_ability) vs DBC (talents).
tags: ["tuning", "skills", "content"]
resource: <server DBC directory>
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
**Related:** [Spells](/content-creation/spells.md) · [Factions, reputation & professions](/content-creation/factions-professions.md)

## §3 — Skills & talents (where they live)

**What is in the DB (tw_world, SQL-editable, permanent) — the main path:**

| Table | Holds | Notes |
| --- | --- | --- |
| `spell_template` | **ALL spells** | **`Spell.dbc` is NOT loaded by the server** — spells are read from this table (`Loading spells...` at boot) |
| `skill_line_ability` | **skill-line abilities** (spells granted by a skill, learn-on-skill, grey/green levels) | **`SkillLineAbility.dbc` is NOT loaded** — this table replaces it (`Loading skill lines...`) |
| `playercreateinfo` | starting location per race/class | |
| `playercreateinfo_spell` | starting spells per race/class (skills are born from these!) | flow: learn → `UpdateSpellTrainedSkills` → skill from `skill_line_ability` |
| `playercreateinfo_action` | starting action buttons | |
| `playercreateinfo_item` | starting items | `INSERT ... (1,1,6948,1)` = hearthstone on a new human warrior |
| `player_levelstats` / `player_classlevelstats` | stats / HP-mana per race-class-level | |
| `player_xp_for_level` | **XP curve (60 levels, custom)** | `UPDATE player_xp_for_level SET xp_for_next_level=... WHERE lvl=...` |
| `exploration_basexp` | exploration XP per level | |
| `creature_template` | mobs: `level_min/max`, `rank`, `xp_multiplier`, `dmg_*`, `health_*`, `gold_min/max` | `UPDATE creature_template SET xp_multiplier=2 WHERE entry=...` |
| `reputation_reward_rate` | rep per faction | |

**What is in the server's DBC directory (host path is deployment-specific; needs a DBC editor + repack):**

- `SkillLine.dbc`, `SkillRaceClassInfo.dbc`, `SkillTiers.dbc` — the skill base (names, who can learn, costs) — loaded
- `Talent.dbc`, `TalentTab.dbc` — **talent trees (DBC only, no DB table)** — loaded
- The audited source's DBC loader uses a fixed subset; `Spell.dbc` and `SkillLineAbility.dbc` are not server data authorities in this fork because their corresponding SQL tables replace them. Verify the pinned source before relying on a count.
- The DB tables `skillline` / `skilllineability` / `skillraceclassinfo` / `talent` / `talenttab` are empty mirrors — editing them does nothing

**Where character skills/spells are saved:** `character_skills` (guid, skill, value, max) and `character_spell` (guid, spell, active, disabled) in tw_char — `.learn` / `.unlearn` persist here on save.

**Shop (Donation Points):**

- Balance: `tw_logon.shop_coins` (`id` = account, `coins`) — script `sudo tortoise-coins`
- History: `shop_coins_history`, `shop_diff`, `shop_logs` (logon)
- **Shop catalog: `tw_world.shop_items`** (`item_id`, `price` in coins, `category`…) + `shop_categories` (Miscellaneous/Skins/Gameplay/Glyphs/Mounts) — adding your own shop items = INSERT into `shop_items`

**Correction (verified 2026-08-11):** `tw_logon.world_config` is **vestigial** — 0 rows, and the core neither reads nor writes it (`LoadConfigSettingsFromDB` has zero callers; `ExportConfigSettingsToDB` is disabled — config comes exclusively from mangosd.conf, see `World.cpp:880-888, 1515`). The claimed per-setting columns (`start_player_level`, `rate_xp_kill`…) do not exist there.
