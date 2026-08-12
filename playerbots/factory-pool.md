---
type: Reference
title: Bot creation pipeline & random-bot pool
description: How bots are created (Randomize phases, race/class/name/gear/professions/talents) and the random-bot pool lifecycle (events, teleports, re-randomize).
tags: ["playerbots", "factory", "pool"]
resource: https://github.com/Shyalya/tortoise-wow/tree/playerbots-integration-gh/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-11T17:20:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

# Bot creation pipeline & random-bot pool

**Related:** [PlayerBots architecture](/playerbots/architecture.md) · [PlayerBots modification](/playerbots/modification.md) · [PlayerBots behavior systems](/playerbots/behavior-systems.md)

## PlayerbotFactory::Randomize() phases (in order)

Prepare (resurrect/combat-stop; `GiveLevel(randombotStartingLevel)` if DisableRandomLevels) → reset (ClearSpells; full wipe of inventory/quests/talents/auras for non-incremental) → InitBags (Traveler's Backpack fill) → InitAvailableSpells (step 1) → InitAllSkills (UpdateSkillsForLevel + InitTradeSkills) → **talents** (SelectPremadeSpecNo → "auto talents"; DbStore reset; ResetStrategies) → InitAvailableSpells (step 2, after talents) + InitSpecialSpells → mounts/reps/taxi (real random bots) → enchants + InitEquipment + gems → ammo/food/potions/reagents + consumables + InitInventory → guild/arena-team → hunter/warlock pet → money → SaveToDB.

- **Race/class**: weighted roll over `AiPlayerbot.ClassRaceProb.<class>.<race>` matrix; **gender** urand(0,1); **name** from `ai_playerbot_names` per race/gender (fallback generated suffix); **appearance** sampled from CharSections DBC. Bulk creation at startup (`CreateRandomBots`).
- **Gear**: from **`ai_playerbot_equip_cache`** (precomputed BiS per class/spec/level/slot via stat weights — `RandomItemMgr` scores every item); filters: item level ≤ RandomGearMaxLevel, req-level diff ≤ RandomGearMaxDiff, equip checks; legendaries blocklisted unless incremental (50% keep); `.bot init [white|green|blue|epic|legendary|sync]` re-randomizes at that quality (sync = copy master's gear score).
- **Professions**: exactly 2 primary (class-tied pools, e.g. warrior → BS+Eng), plus First Aid/Fishing/Cooking; **all affordable trainer recipes** learned (every tradeskill trainer, GREEN state).
- **Talents**: premade spec builds ALWAYS (weighted pick among configured paths); randomness only chooses WHICH premade path — no point-by-point random builds.
- **Spells**: default + class level spells (core trainer progression), hardcoded fixes (Polymorph pig/turtle ≥60, druid forms, vanilla book spells at 60), `randomBotSpellIds` from config.

## Random-bot pool lifecycle (ai_playerbot_random_bots events)

| Event | Meaning |
| --- | --- |
| `add` | bot allowed in world; TTL min/maxRandomBotInWorldTime; `IsRandomBot` check |
| `login` / `logout` | async login marker / timed-offline marker |
| `update` | per-bot processing tick |
| `randomize` | full re-randomize schedule (min/maxRandomBotRandomizeTime) |
| `teleport` | teleport schedule (min/maxRandomBotTeleportMin/MaxInterval) |
| `change_strategy` | strategy-change cycle |
| `bot_count` | global target population, re-rolled every count-change interval |
| `dead`/`revive` | death bookkeeping |
| `sellmultiplier`/`buymultiplier` | AH price multipliers |

Plus values: `current_time` (global clock driving event expiry), `specNo`, `specLink`, `level`, `firstSkill`, `secondSkill`, `weaponType`, `version`, `always`, `selfbot`. (No `bg`/`lfg` event names in this tree.)

**Transitions:** startup creates the roster → `AddRandomBots` tops up to `bot_count` (gated by RandomBotsMaxLoginsPerInterval) → activity scaling (level-sync with online players) → timed logout when no players online (group members +120 s) → idle + expired `randomize` → full re-randomize at random level (`RandomizeFirst`) or incremental gear update → idle + expired `teleport` + players online → `RandomTeleportForLevel` + inn binding.

**Near-player behavior:** `RandomBotTeleportNearPlayer` (default OFF) filters teleport candidates to active zones (with real players) with density caps — runs on the bot's own 2–48 h schedule, NOT on player login. On login the core only greets grouped bots (`hello` text); `hello_follow` is the greeting when a bot follows its master after joining.

## ai_playerbot_db_store (presets)

Per-bot key/value state: saves AiObjectContext values (`key='value'`, payload `name>text`) + strategy lists under keys `co`/`nc`/`dead`/`react`; presets via `.bot save/load <preset>` (default `""`); auto-save on logout-with-master, strategy changes, keep-item, reset; auto-load on ResetStrategies when the bot has a player relation.
