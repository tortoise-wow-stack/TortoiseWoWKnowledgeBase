---
type: Reference
title: Hot-reload commands
description: The full .reload table list \u2014 what can change without a restart.
tags: ["ops", "reload"]
resource: ssh://<server>
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
**Related:** [Content creation](/content-creation/index.md) · [Console](/ops/console.md)


## §9 — Hot-reload commands (no restart; console: `reload <table>`)

Turtle additions: `shop`, `bgplayers`, `gmlevels`, `gm_ticket_template`, `housing`, `visibilities`.

Content (vmangos set): `creature_template`, `creature`, `creature_questrelation`, `creature_involvedrelation`, `creature_loot_template`, `creature_onkill_reputation`, `creature_groups`, `creature_spells`, `creature_ai_events`, `gameobject`, `gameobject_questrelation`, `gameobject_involvedrelation`, `gameobject_loot_template`, `gameobject_requirement`, `gameobject_scripts`, `item_template`, `item_loot_template`, `item_enchantment_template`, `item_required_target`, `quest_template`, `quest_start_scripts`, `quest_end_scripts`, `quest_greeting`, `npc_vendor`, `npc_trainer`, `npc_gossip`, `npc_text`, `gossip_menu`, `gossip_menu_option`, `page_text`, `game_tele`, `game_weather`, `areatrigger_*`, `points_of_interest`, `reference_loot_template`, `fishing_loot_template`, `skinning_loot_template`, `pickpocketing_loot_template`, `disenchant_loot_template`, `mail_loot_template`, `reputation_reward_rate`, `reputation_spillover_template`, `skill_fishing_base_level`, `spell_affect`, `spell_area`, `spell_chain`, `spell_elixir`, `spell_learn_spell`, `spell_pet_auras`, `spell_proc_event`, `spell_proc_item_enchant`, `spell_script_target`, `spell_scripts`, `spell_target_position`, `spell_threats`, `spell_disabled`, `spell_mod`, `spell_group`, `spell_group_stack_rules`, `exploration_basexp`, `conditions`, `mangos_string`, `autobroadcast`, `petitions`, `variables`, `config` (re-reads mangosd.conf!), `locales_*`…

**No `reload spell_template`** — spells load at boot only (config/`spell_mod` etc. ARE hot-reloadable).
