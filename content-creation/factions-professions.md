---
type: Reference
title: Factions, reputation & professions
description: DB-driven factions, rep rates, skill_line_ability, crafting flow, reloads.
tags: ["content", "factions"]
resource: mariadb://tw_world/faction
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
**Related:** [Skills & talents](/tuning/skills-talents.md) · [NPCs](/content-creation/npcs.md)


## §19 — Factions, reputation, professions (verified)

**Factions = DB tables, NOT DBC** (Faction.dbc/FactionTemplate.dbc are NOT loaded!):

- `faction` (id, `reputation_list_id` (-1 = no rep UI), `base_rep_race_mask1..4`/`base_rep_class_mask1..4`/`base_rep_value1..4` (start standing per bucket), `reputation_flags1..4`, `team` (parent faction), `name1..8`, `description1..8`) — no base_rep_rank column here.
- `faction_template` (id, `faction_id`, `faction_flags`, `our_mask`, `friendly_mask`, `hostile_mask`, `enemy_faction1..4`, `friend_faction1..4`). Masks: PLAYER=1, ALLIANCE=2, HORDE=4, MONSTER=8. Friendly = mask overlap or explicit list; hostile likewise.
- **Custom faction** = 1 row in `faction` + 1 in `faction_template` → **restart** (no reload for factions). Client caveat: rep UI names come from the client's MPQ Faction.dbc — new factions need client patching (mirror tables `factiongroup`/`factiontemplate` feed the TurtlePatcher pipeline).

**Reputation:** gains = base × level-diff penalty × source rate (`reputation_reward_rate`: quest_rate/creature_rate/spell_rate; ≤0 = disabled) × `Rate.Reputation.Gain`. Spillover via `reputation_spillover_template` (factionN, rate_N, rank_N). Per-char: `character_reputation` (guid, faction, standing, flags); ranks from −42000 (PointsInRank {36000,3000,...}).

**Professions:** skills from `SkillLine.dbc` (loaded) + **`skill_line_ability`** (DB): `skill_id, spell_id, race_mask, class_mask, req_skill_value, superseded_by_spell, learn_on_get_skill (1 = auto-learned with the profession), max_value, min_value, req_train_points`. Profession = spell with effect1 = SPELL_EFFECT_SKILL (36); trainer rows must have effect0 = LEARN_SPELL. Crafting: recipe spell in spell_template with `reagent1..8`/`reagentCount1..8` + effect = CREATE_ITEM (24); reagents validated/consumed at cast; skill value enforced at LEARN time only.

**Reload:** `npc_trainer(+template)`, `reputation_reward_rate`, `reputation_spillover_template`, `player_factionchange_*`, `spell_learn_spell` ✓ — **no reload for faction/faction_template/skill_line_ability/spell_template** (restart).
