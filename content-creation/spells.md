---
type: Reference
title: Spells
description: spell_template columns, validation, client-side needs, no reload (restart).
tags: ["content", "spells"]
resource: mariadb://tw_world/spell_template
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
**Related:** [Skills & talents](/tuning/skills-talents.md) · [Quests](/content-creation/quests.md)


## §16 — Content creation: Spells (verified live)

**spell_template** — effects are INLINE (`effect1..3`, max 3); NO separate spell_effect table. Fork quirk: **column names differ from vanilla conventions** — `school` (not SchoolMask), `effect1`, `effectApplyAuraName1`, `effectBasePoints1`, `manCostPerLevel`, `effectDicePerLevel1` (loader reads positionally). Extra: `spell_effect_mod` (per-effect overrides, -1 = inherit), `script_name`, locales in `locales_spell`.

**Key columns:** `entry`, `school` (1 phys 2 fire 4 frost…), `category`, `castingTimeIndex`/`durationIndex`/`rangeIndex` (→ client DBCs — reuse a sibling spell's values), `spellVisual1`, `spellIconId` (→ SpellIcon.dbc), `spellPriority`, `name`, `description`, `powerType`, `manaCost`, `recoveryTime`, `categoryRecoveryTime`, `procFlags/Chance/Charges`, `stackAmount`, `reagent1..8(+Count)`, `spellLevel`/`baseLevel`/`maxLevel`, `dmgMultiplier1..3`; effects: `effect`, `effectDieSides`, `effectBaseDice`, `effectBasePoints`, `effectBonusCoefficient`, `effectMechanic`, `effectImplicitTargetA/B`, `effectRadiusIndex`, `effectApplyAuraName` (33=slow, 6=mod speed…), `effectAmplitude`, `effectChainTarget`, `effectItemType`, `effectMiscValue`, `effectTriggerSpell`, `effectPointsPerComboPoint`. Enum values: SPELL_EFFECT_CREATE_ITEM=24, LEARN_SPELL=36, SCHOOL_DAMAGE=2, APPLY_AURA=6; auras per SpellAuraDefines (MOD_DECREASE_SPEED=33).

**Validation:** load-time has NO checks (raw positional fill); the real gate is `IsSpellValid()` used by `.learn` — rejects only: create-item effect without item_template row, learn-spell effect pointing at an invalid spell, craft reagents missing from item_template. **No aura/target validation in this fork.**

**Client-side:** the server is 100% DB-driven, but the 1.18.1 client looks up its OWN `Spell.dbc` by spell id for tooltip/icon/animation/targeting UI. A new spell id casts and functions server-side with fallback visuals; for proper UI you need a client Spell.dbc row (or remap an existing entry's `spellIconId`/`spellVisual1`). The base dump was originally exported FROM client Spell.dbc (spell_data/spell_template.csv).

**Reload: NO `reload spell_template`** — spell changes need a core restart. Learned spells persist in `character_spell` (auto-purged if the spell vanishes). `.learn <id> [all] [force]` requires a valid spell.

**Minimal recipe:** `INSERT INTO spell_template (entry, school, spellLevel, castingTimeIndex, rangeIndex, powerType, manaCost, effect1, effectBasePoints1, effectImplicitTargetA1, spellIconId, spellVisual1, name, description) VALUES (...)` (reuse sibling spell's indexes/icon/visual) → restart core → `.learn <entry>`.
