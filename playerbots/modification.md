---
type: Reference
title: PlayerBots modification
description: Config keys inventory, SQL tables, custom strategy/action pattern, texts, travel data.
tags: ["playerbots", "modding"]
resource: https://github.com/Shyalya/tortoise-wow/tree/playerbots-integration-gh/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---
**Related:** [PlayerBots config](/playerbots/config.md) · [PlayerBots architecture](/playerbots/architecture.md)

## §23 — PlayerBots: how to MODIFY (config/SQL/code)

**Config:** configuration is broad and build/deployment-specific; this document does not treat configuration keys as commands. For the command-affecting subset, see [command config](command-config.md). Core families include population, timing, combat defaults (`CombatStrategies`/`RandomBotCombatStrategies`/`NonCombatStrategies`), automation, gear, economy/chat, jumps, and performance. Source baseline counts and compile-time conditions are in [registry](registry.md).

**SQL data — character database:** `ai_playerbot_names`, `guild_names`, `arena_team_names`, `equip_cache` (best-in-slot candidates per class/spec/level/slot), `rarity_cache`, `rnditem_cache`, `tele_cache` (safe teleport spots), `item_info_cache`, `db_store` (per-bot key/value presets), `random_bots` (roster/events), `custom_strategy`, and `ahbot_*`. **World database:** `ai_playerbot_texts` (chatter), `texts_chance`, `help_texts`, `rpg_races`, `indexes`; classic-only travel tables include `ai_playerbot_travelnode`, `_link`, `_path`, `_named_location`, `_enchants`, `_weightscales`, and `_zone_level`. Dataset sizes are build/deployment facts; query the pinned database when capacity or migration work depends on them.

**Code-level custom strategy/action (the pattern):** register in `StrategyContext.h` / `ActionContext.h` (`creators["name"] = [](PlayerbotAI* botAi){ return new XStrategy(botAi); };`); subclass `Strategy` (getName + InitCombat/NonCombat/DeadTriggers filling `TriggerNode`s: `new TriggerNode("trigger", NextAction::array(0, new NextAction("action", relevance), NULL))`); subclass `Action` (Execute(Event&), isPossible/isUseful/prerequisites). Copy examples: `EmoteStrategy.h/.cpp` + `EmoteAction.h/.cpp`. Relevance priorities: ACTION_IDLE 1 … ACTION_PASSTROUGH 100.

**`custom::` mechanism:** NOT a fixed list — any `custom::<name>` instantiates `CustomStrategy`; behavior from `ai_playerbot_custom_strategy` rows (tw_char): `action_line` format `trigger>action!relevance,action2!rel`; per-owner rows override `owner=0`; in-game editing via `cs <name> <idx> <command>` chat command. Shipped: only `custom::say` (6 lines).

**Premade specs:** generator `tools/talents/build_premade_specs.py --dbc <dir> [--rate N]` — hand-built BUILDS dict (class → spec → lvl-60 link), LEVELS 10..60, outputs the config block; `--rate` must match `Rate.Talent`.

**Bot chatter:** all speech in `ai_playerbot_texts` (name key, text, say_type 0=say/1=yell, reply_type, 8 locales); emitted via `BOT_TEXT("name")` with `%placeholder` substitution; `texts_chance` throttles (taunt 30, aoe 75, loot 20). Add chatter = INSERT row + reference the name.

**Travel data:** SQL-shipped, runtime-regenerable (regenerates only when `linked=0`/`calculated=0`/missing; needs maps/vmaps/mmaps; writes back via PExecute; can dump travelNodes.csv).
