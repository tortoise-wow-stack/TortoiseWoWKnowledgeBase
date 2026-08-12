---
type: Reference
title: PlayerBots chat commands and parsing
description: "Complete source-verified chat trigger names, aliases, routing, parsing, and timing behavior."
tags: ["playerbots", "chat", "commands"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


Bots receive plain `SAY`, `YELL`, `WHISPER`, `PARTY`, `RAID`, `GUILD`, and channel chat through the speaker's session hook. Incoming `CHAT_MSG_ADDON` is dropped. Incoming `LANG_ADDON` is ignored unless the text starts with `BOT\t`; this accepts the mangosbot compatibility marker but does not make `SendAddonMessage` a command transport.

## Delivery and targeting

* WHISPER is name-targeted: whisper the bot's exact name from any distance subject to normal command/security gates.
* SAY reaches same-map bots within 25 yards; YELL reaches same-map bots within 300 yards.
* PARTY/RAID reaches bots for which the speaker is in the group; GUILD reaches same-guild bots; channel chat additionally requires channel membership. Random-bot dispatch applies team filtering and only sends to random bots whose AI master is the speaker. Owned bots are dispatched by the speaker's PlayerbotMgr.
* The first security gate is INVITE; after parsing/filtering, non-unsecured commands require ALLOW_ALL. Unsecured prefixes are `who`, `where`, `wts`, `sendmail`, `invite`, `leave`, `join`, `lfg`, `guild invite`, and `guild leave`. `debug <query>` returns before the ALLOW_ALL gate.

## Exact trigger registry (137 keys, 129 distinct destination commands)

The keys below are the complete `ChatTriggerContext` registration at this commit. Matching is prefix-based at word boundaries and longest-prefix parsing from the end; trailing text becomes the parameter. Aliases map to the destination in parentheses:

```text
quests, quest reward, stats, leave, rep (reputation), reputation, log, los, drop, roll, share,
q, ll, ss, loot (add all loot), add all loot, release, corpse run, teleport, taxi, repair,
u (use), use, c (c), items (c), inventory (c), inv (c), e (e), equip (e), keep, ue, s, b, bb,
r, t, nt, talents, spells, co, nc, de, react, all, trainer, attack, attack rti, pull, pull rti,
chat, accept, home, load ai, list ai, save ai, reset ai, reset strats, reset values, destroy,
emote, buff, help, gb (gb), gbank (gb), bank, follow, wander, stay, guard, free,
wait for attack time, pet, focus heal, follow target, boost target, buff target, revive target,
self res, flee, grind, tank attack, talk, cast, castnc, invite, join, lfg, spell, rti, revive,
runaway, warning, position, summon, who, where, save mana, max dps, possible attack targets,
attackers, formation, stance, sendmail, mail, outfit, go, ready (ready check), debug, cdebug,
cs, wts, hire, craft, flag, range, ra, give leader, cheat, rtsc, ah, ah bid, guild invite,
guild join, guild promote, guild demote, guild remove, guild leave, guild leader, bg free,
move style, jump, doquest, skill, faction, set value, glyph, speak
```

`repop` is **not** a chat trigger in this registry. It is a ChatActionContext action and is reached by `do repop`; a bare `repop` falls through parseable-item/help fallback rather than invoking that action.

## Parsing and inline controls

* `follow me` is parsed as trigger `follow` with parameter `me`; multiword names are attempted before shorter prefixes. Item/spell/quest/help links are extracted by `ChatHelper::parseValue("command", ...)`. Parseable links and recognized item/money text can fall back to `c`/`t` query actions.
* `d <action>` and `do <action>` execute an action immediately in `HandleCommand`; `do` in a parsed `.bot cmd` route is queued through `ExternalEventHelper` instead.
* The configured `AiPlayerbot.CommandSeparator` (default `\`) recursively splits stacked commands. `AiPlayerbot.CommandPrefix` (default empty) must prefix every command when configured.
* `queue <cmd>` queues a command at `now + group-position-index` seconds and is deliberately disabled for whispers (`type != CHAT_MSG_WHISPER`). `reset`, `logout`, `logout cancel`, and `wait <seconds>` are special inline controls. Wait over 20 seconds returns exactly `Max wait time is 20 seconds!`; success says `Waiting for <seconds> seconds!`.
* `#w `, `#p `, `#r `, `#a `, `#g ` set the reply route for three seconds and require the trailing space. `#a` does not send a native addon-channel response from ordinary chat; the tell path emits `BOT\t` + text as PARTY with `LANG_ADDON`. The synchronous `debug` path below is the direct `CHAT_MSG_ADDON` response.
* `warning` is synthesized for RAID_WARNING containing the bot name unless it contains `award`.

Unknown whisper triggers are silently dropped: the code's unknown-command tell is commented out. A failed action can also produce no tell, especially with `silent` strategy, deduplication (`RepeatDelay`, default 5000 ms), teleporting requesters, or failed security checks. Chat reply queue delays BOT_TEXT-driven chatter by 10–20 seconds out of combat and 15–30 seconds in combat; direct tells and the `debug` packet are not subject to that queue delay.

Source distinction: these are user-operable trigger/action names, not the internal values/triggers in `strategy/TriggerContext.h` and `ValueContext.h`.
