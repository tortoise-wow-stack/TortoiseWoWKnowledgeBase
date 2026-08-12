---
type: Reference
title: PlayerBots ownership, security, and failures
description: "Source-verified ownership/security ladder and exact important failure strings for operators and addon authors."
tags: ["playerbots", "security", "errors"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


## Security ladder

`DENY_ALL (0) < TALK (1) < GUILD (2) < INVITE (3) < ALLOW_ALL (4)`.

`PlayerbotSecurity::LevelFor` grants ALLOW_ALL to rank `>= SEC_GAMEMASTER` (rank 4 in this port), the bot's own account, and a group member of that bot. Opposing-faction requests are DENY_ALL unless `CONFIG_BOOL_ALLOW_TWO_SIDE_INTERACTION_GROUP` is enabled; same-faction does not need a special exception. Level gap, gear-score difference (when enabled), battleground queue, and LFG queue can reduce an otherwise ordinary requester to TALK. An ungrouped bot gives strangers INVITE; a full group gives GUILD; a bot in a group led by someone else gives GUILD; a bot that is group leader gives INVITE.

The chat handler first requires INVITE (silent for non-whispers), then requires ALLOW_ALL for ordinary commands. The unsecured prefixes are exactly `who`, `where`, `wts`, `sendmail`, `invite`, `leave`, `join`, `lfg`, `guild invite`, `guild leave`. `debug <query>` is intentionally before the ALLOW_ALL check; it still needs the first gate. `cheat` action itself checks GM security. `.bot reload` and `.bot tweak` check GM; `.bot self` checks `SelfBotLevel`; `.bot debug` is **not** handler-level GM-gated despite stale source help text.

## Ownership paths

* Same-account alts are owned by the caller's PlayerbotMgr and can be controlled through `.bot` when account ownership resolves. `AllowMultiAccountAltBots` plus guild membership can permit cross-account guild bots; `AllowGuildBots=false` blocks that route. `.rndbot` refuses a non-random alt through its manager for non-admin callers with `Can not control alt-bots with this command.`
* Random-pool bots are managed by RandomPlayerbotMgr. A real player may acquire one through group/invite paths; random dispatch only sends ordinary chat to bots whose AI master is the speaker.
* `.bot summon/recall/come` allows same-account, random, or explicitly master-linked bots only. It refuses offline bots and cross-instance pulls; see exact strings below.
* Master logout invokes bot logout handling; replies to a logged-out master can disappear.

## Exact important failures

| Situation | Exact source text or behavior |
| --- | --- |
| system disabled | `Playerbot system is currently disabled!` for `.bot`; random handler logs the same error and returns false |
| no active session / manager | `You may only add bots from an active session`; `you cannot control bots yet` |
| ownership | `Not in your guild or account`; `Can not control alt-bots with this command.`; `Not your bot` |
| target resolution | `you must be in group`; `you must be in a guild`; `No guild members`; `character not found`; `Unknown command. Use 'help' for more information.` |
| summon offline | `Bot is offline (use \`.bot add <name>\` first)` |
| summon ownership | `This bot isn't yours to summon.` |
| summon state | `Bot is in combat — wait for it to settle.`; `Bot is in BG / BG queue.`; `Bot is in an instance — can't pull cross-instance.` |
| security whisper | `I'm kind of busy now`; `I'll do it later`; `You are too low level: <colored lv>/<colored botLv>`; `Your gearscore is too low: <colored values>`; `I have a master already`; `You are a bot`; `You are the enemy`; `Invite me to your group first`; `I am in a full group. Will do it later`; `I am currently leading a group. I can invite you if you want.`; `I am in a group with <name>. You can ask him for invite.` / `I am in a group with someone else`; `I am in a queue for BG. Will do it later`; `I am in a queue for dungeon. Will do it later`; `I can't do that` |
| action | `do requires a bot`; `Bot has no AI`; `action not found`; `action failed`; `(no output)` |
| command bridge | `Sending command <param> to player <bot>`; `command failed` |
| wait | `Max wait time is 20 seconds!` |
| remote query | `invalid command: <command>`; TCP `invalid request: <request>`; TCP `invalid guid` |

Color escape codes, punctuation, whitespace, and human-readable output are not a stable semantic API. Preserve raw text for logs, normalize for display, and use explicit sentinel strings only as best-effort diagnostics.
