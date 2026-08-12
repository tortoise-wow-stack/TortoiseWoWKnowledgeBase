---
type: Reference
title: PlayerBots .bot and .rndbot commands
description: "Exact source-verified console command handlers, aliases, parameters, targeting, and important return contracts."
tags: ["playerbots", "commands"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


**Invocation:** the core registers both `.bot` and `.rndbot` at `SEC_PLAYER`; `.rndbot` dispatches random-pool handlers first and then falls through to the same PlayerbotHolder command engine. `.ahbot` is a separate `SEC_MODERATOR` command and is not a PlayerBots control surface. Source: `src/game/Chat/Chat.cpp` command table; `PlayerbotMgr.cpp`; `RandomPlayerbotMgr.cpp`.

## Target grammar

`.(rnd)bot <command> [target] [parameters]`.

* No target uses the current target only when it is a non-real-player bot; otherwise help is returned.
* `*` targets every other member of the caller's group; without a group: `you must be in group`.
* `guild` targets character rows in the caller's guild; without a guild: `you must be in a guild`; no DB result: `No guild members`.
* `!` targets online holder bots only when security is **strictly greater than** `SEC_GAMEMASTER` (this port aliases `SEC_GAMEMASTER` to rank 4 `SEC_ADMINISTRATOR`; therefore rank 5 `SEC_SIGMACHAD` or rank 6 console, not an ordinary rank-4 GM). `add`, `login`, and `delete` also allow matching offline holder entries in this branch.
* A character name targets that character. Names may be comma-separated. If the first target token is an account username, it expands to every character on that account.
* `command=subtype` passes `subtype` as the handler parameter; otherwise remaining text after the target is the parameter.
* Each resolved target produces `<command>: <bot> - <result>`. Unknown names produce `character not found`; unknown handler names produce `unknown command`.
* `.rndbot` pool-specific player handlers match the bot name by **prefix**; omitted name defaults to `%` and therefore matches every random bot.

## Holder commands (no bot target)

`list`, `help`, `reload`, `tweak`, `self`, `spoof`, `p`, `g`, `r`, `rl`, `create`, `group`; `runtest` exists only with `GenerateBotTests`.

* `reload` and `tweak` require `security >= SEC_GAMEMASTER`; failure is `You do not have permission to use this command.`
* `self [login]` toggles AI on the caller. `self login` additionally persists self-bot-on-login state. `SelfBotLevel` controls disabled/GM-only/any-player behavior.
* `spoof <online-name>` redirects holder commands; empty clears it. Exact failures include `Player '<name>' not found.`, `Player '<name>' found but is not online.`, and `Spoof is not set.`
* `p`, `g`, `r`, `rl` send party/guild/raid messages or raid leadership requests as a bot/sender. With no message, `p/g/r` return party/guild/raid info. They require a corresponding group/guild/raid and return exact `No sender found`, `Sender is not in a group`, `Sender is not in a guild`, `Sender is not in a raid group` where applicable.

### `create`

`.bot create [name=N] [faction=alliance|horde] [race=R] [class=C] [gender=male|female|0|1] [level=N] [role=tank|healer|dps] [login=0|1|true|false|yes] [group=character] [gear=value] [test=name] [temporary=0|1]`.

Names/classes/races accept case-insensitive names and, for class/race (and gender/team where implemented), valid numeric IDs. Unknown values fall back to the parser's none/default behavior. `role=` drives initial talent selection; it is not a universal runtime strategy.

`.bot group [size=N] [other create key=value...]` creates until the master plus bots reaches `size` (default `5`, i.e. four bots), selecting complementary role/class candidates. If the account is full or creation fails, source returns messages such as `Account has max characters`, `Name already exists`, or `Failed to create character`.

## Per-bot commands and parameters

Aliases are grouped by handler:

| Handler | Commands | Parameters / result |
| --- | --- | --- |
| Login/add | `add`, `login` | asynchronous login request; common results `ok`, `Player already logged in`, `Add: Error parsing <param>`, `Not in your account` |
| Remove | `remove`, `logout`, `rm` | `ok`, `Player is offline`, ownership/binding failures |
| Delete | `delete` | deletes character; `ok`, `Not your bot`, or parse failure |
| Gear | `gear`, `equip` | empty/default random; `white/common`, `green/uncommon`, `blue/rare`, `purple/epic`, `upgrade`, `sync`, `best`, `partial`; unknown: `unknown gear command` |
| Train | `train`, `learn` | learns class-level spells; `class level spells learned` |
| Food | `food`, `drink` | adds food/drink; `food added` |
| Potions | `potions`, `pots` | `potions added` |
| Consumables | `consumes`, `consumables`, `consums` | `consumables added` |
| Reagents | `regs`, `reg`, `reagents` | `reagents added` |
| Prepare | `prepare`, `prep` | refreshes preparation; `consumes/regs added` |
| Init | `init` | bare = full randomize; `white/common`, `green/uncommon`, `blue/rare`, `epic/purple`, `legendary/yellow`, `sync`; returns `ok` (an unknown non-empty parameter also falls through to `ok` without a documented effect) |
| Enchants/ammo/pet | `enchants`, `ammo`, `pet` | applies enchants, initializes ammo, or initializes pet/spells; `ok` |
| Level/random | `levelup`, `level`, `random` | randomize/level update; `ok` |
| Summon | `summon`, `recall`, `come` | online bot only; `ok — teleporting to you` or exact failures in [security/failures](security-failures.md) |
| Offline AI | `always` | toggles offline character AI; see [lifecycle](bot-lifecycle.md) |
| Debug chat action | `debug` | synchronous captured chat-action output; note that source help says GM-only but handler has no handler-level GM check |
| C++ chat-command bridge | `c` | executes `cdebug` with `monstertalk <param>`; returns `ok` after dispatch |
| Whisper bridge | `w` | sends a queued whisper; no message returns bot classification/name/level/race/class info; message returns `Sending whisper <msg> to player <receiver> from <sender>` |
| Queued command | `cmd` | parses a chat command through `ExternalEventHelper`; success `Sending command <param> to player <bot>`, parse failure `command failed` |
| Build test | `test` | empty returns usage and two built-in names; otherwise `Test '<name>' started for bot <bot>` |
| Synchronous action | `do` | exact output/error behavior in [actions/strategies](actions-strategies.md) |
| Recording | `record`, `read`, `clear` | enable recording; read `(no messages)` or captured lines; clear `Messages cleared` |

`refresh` appears in help and is implemented as a handler in this source but is not in the holder map shown at construction; do not rely on `.bot refresh` unless the build exposes it through another path.

## `.rndbot` pool commands

The random manager checks these prefixes before holder fallback:

* Console/global: `help [command]`, `reset`, `stats`, `update`, `pid p i d`, `diff [player_diff] [empty_diff]`, `clean map`, `login debug`.
* Per-random-bot (name prefix; omitted name `%`): `init`, `upgrade`, `refresh`, `teleport`, `rpg`, `revive`, `grind`, `change_strategy <botname> <strategy>`, `remove <botname>`.
* `cmd <botname> <command>` is documented by random help and reaches holder fallback; `help commands` enumerates the complete random help map.

`stats` requires a numeric GUID parameter internally. Client `.rndbot stats` substitutes the caller's player GUID, returns `Stats requested.` immediately, and launches detached output; it is not a synchronous stats payload. `pid` is a real command, not a typo.

## Stable-vs-human output

System-chat lines and handler strings above are source contracts useful for diagnostics but not a versioned API. Preserve exact matching only for the explicitly listed sentinel errors; normalize colors/newlines and tolerate added text. Action/chat responses can be empty, delayed, split, or strategy-suppressed.
