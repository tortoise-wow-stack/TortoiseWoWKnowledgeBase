---
type: Reference
title: PlayerBots actions, strategies, and state-query surfaces
description: "Source-verified public action/strategy registries and exact state-query responses, with build-conditional counts."
tags: ["playerbots", "actions", "strategies", "addon"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


## Public action vocabulary (`do`)

`.bot do <bot> <action> [action-parameter]` resolves the longest action name available in that bot's shared and class/build contexts, executes synchronously, records tell output, and joins recorded lines with newlines. It returns:

* `do requires a bot`, `Bot has no AI`, `action not found`, or `action failed`;
* `(no output)` as the exact sentinel when execution succeeds without recorded output;
* recorded human-readable lines when output exists.

Normal source build (`GenerateBotTests` **off**) registers **272** generic actions in `ActionContext`, **128** chat actions in `ChatActionContext`, and **53** world-packet actions in `WorldPacketActionContext`; their shared set union is **450** unique names (there are overlaps). `test` adds one source-visible creator under `GenerateBotTests`, making the source shared union 451. Class `AiObjectContext` action factories add 675 unique source-visible names; the complete pinned source union is 1,126 names. A Classic bot receives the shared contexts plus only its compiled class contexts, so no bot exposes the entire source union. Counts are registrations, not promises that every action is possible for every class/state.

The public action families include movement/travel, combat/targeting/pull, loot, item/equipment/consumables, social/group/guild/mail/AH, questing, BG/vehicle/fishing, racial abilities, state/reset/value tools, and raid/dungeon encounter actions. See the generated [public action catalog](action-catalog.md) for every shared and class registration name at the pinned commit. Runtime execution still applies class, expansion, state, target, spell, gear, map, packet, and security prerequisites.

## Strategies and change syntax

`co`, `nc`, `de`, `react`, and `all` are ChatActionContext actions. Their strategy parameters use `+name` add, `-name` remove, and `~name` toggle; sibling strategy contexts may remove incompatible siblings. `co +tank`/`+heal`/`+dps` are **class-dependent**: this source defines tank placeholders for warrior/paladin/druid/deathknight (WoTLK only), heal for paladin/priest/shaman/druid, and dps for priest; mage/rogue/hunter/warlock do not define those role placeholders, so an unknown strategy can be silently ignored. `ranged` is generic. Prefer class-specific keys from the bot's class context or use `@tank/@heal/@dps` for audience selection.

Build registry counts at this commit:

* Generic `StrategyContext`: 124 creators including `test`; **123 normal-build** generic keys. Movement/assist/quest/fish sibling contexts add 7+3+2+2 = 14 keys, all distinct from the generic context, for **137** normal-build generic/sibling names.
* Class strategy creators (all class `AiObjectContext.cpp` strategy registrations, unique union): **643** names including class-specific aliases/situations when the ten source class directories are considered; subtract the 11 death-knight names for the Classic/MaNGOS Zero source set. These are not all simultaneously available to one bot: each bot gets its own class context and compile-time expansion. See the generated [strategy catalog](strategy-catalog.md) for every source registration grouped by shared/class context.
* `debug` strategy variants are **16**, not 17: `debug`, `debug action`, `debug equip`, `debug grind`, `debug llm`, `debug log`, `debug logname`, `debug loot`, `debug mount`, `debug move`, `debug rpg`, `debug spell`, `debug stuck`, `debug threat`, `debug travel`, `debug xp`.
* `runtest` holder command, `test` strategy, and `test` action are behind `GenerateBotTests`; the source checkout's default Classic build does not imply they exist.

`debug values` is a diagnostic dump of created `ValueContext` objects. It is not a command registry: source has 332 value creators in `ValueContext`, plus generic/class contexts may create more. `state`, `position`, `tpos`, `target`, `hp`, `combat`, `strategy`, `action`, `values`, `travel`, `traveldetail`, and `budget` are the supported remote query names described next.

## Remote state-query API

`PlayerbotAI::HandleRemoteCommand` is shared by TCP, in-game `debug <query>`, and the debug action fallback. Exact commands:

| Query | Response |
| --- | --- |
| `state` | `combat`, `dead`, `non-combat`, or `unknown`; reaction is returned as `unknown` |
| `position` | `<x> <y> <z> <mapId> <orientation>` optionally followed by `\|<zone-name>\|` (enUS source table) |
| `tpos` | target coordinates in the same five-field format, or empty if no current target |
| `target` | target name, or empty |
| `hp` | `<botPercent>%` or `<botPercent>% / <targetPercent>%`, integer truncation |
| `combat` | verbose `UNIT_FLAG_IN_COMBAT: SET\|clear, IsInCombat(): true\|false, CMaNGOS attackers: <n>, victim: <name>\|none \| BotAI: current target: <name> (<guidLow>), invalid: YES\|no\|none, has attackers: true\|false \| Selection: <guidLow>` |
| `strategy` | current engine's newline-separated strategy listing |
| `action` | last action name |
| `values` | `{name=value}\|...` dump of created, formatable values (can be very large) |
| `travel` | optional `<member>'s`, `Target: <title>`, optional status line with `ready`, `preparing`, `traveling`, `forced traveling`, `working`, `cooldown`, or `expired`, seconds left, and retry counts |
| `traveldetail` | multi-line travel short name/title/distance/location/status/conditions; human-readable |
| `budget` or `budget<substring>` | money line plus purpose rows (`repair`, `ammo`, `spells`, `travel`, `consumables`, `gear`, `guild`, `tradeskill`, `skilltraining`, `ah`, `mount`); substring filtering is source `command.find("budget")` behavior and should be sent as `budget<substring>` (a space after `budget` becomes part of the substring) |
| anything else | `invalid command: <command>` |

`combat`, `strategy`, `action`, `values`, `travel`, `traveldetail`, and `budget` are human-readable/unstable contracts. Parse only the simple sentinel/enumeration/field formats where your client can tolerate added fields, locale, empty values, and newlines.
