---
type: Reference
title: PlayerBots offline alts and random-bot lifecycle
description: "Source-verified distinction between owned/offline alternate characters and the random-bot pool."
tags: ["playerbots", "lifecycle", "ownership"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


## Owned/player alt bots

`.bot add/login <character>` creates or queues a PlayerbotAI for a character controlled through the caller's `PlayerbotMgr`. Same-account ownership is automatic; cross-account guild access depends on `AllowGuildBots` and `AllowMultiAccountAltBots`. `.bot add` returns `ok` before asynchronous login has necessarily reached the world. Use `.bot list`, a later command, or a `debug state` query after the bot is online to confirm readiness. Master logout invokes logout handling for owned bots.

`.bot self` turns the current real player character into a bot while the player is in-world. `self login` records the selfbot-on-login flag. `.bot always <player>` uses the random manager's `always` event/value and `freeAltBots` list to keep a logged-out character's AI active; this is an offline/free-alt mode, not a random-pool bot. It can be disabled with the same command and returns `Enabled offline player ai for <name>` / `Disabled offline player ai for <name>`, or `Self-bot is disabled` / `Unable to find player.`.

## Random pool bots

Random bots are characters identified by `IsInRandomAccountList` and managed by `RandomPlayerbotMgr`. Their pool commands (`.rndbot init/upgrade/refresh/teleport/rpg/revive/grind/change_strategy/remove`) operate on matching online pool entries; omitted name is `%` and matching is name-prefix based. A real player can acquire a random bot through invite/group behavior, after which its AI master controls ordinary chat dispatch. Random pool bots are the only bots visible to the optional TCP command server.

`RandomBotGroupNearby` and `RandomBotInvitePlayer` default true in source; nearby invite behavior and level-difference policy are behavior/config concerns, not a guarantee that a particular runtime pool is populated. Random manager actions such as `stats` can be asynchronous or print to server output rather than return data to the initiating chat.

## Do not conflate these paths

* `.bot add` is a character login/control operation; `.rndbot add` may route to RandomPlayerbotMgr and can be asynchronous.
* `.bot always` changes offline alt AI persistence; it does not add a character to the random account pool.
* TCP `<guidLow>` resolves only `GetPlayerBot` in the random pool; owned alts are unreachable there.
* `.rndbot` holder fallback intentionally rejects non-random alt bots for non-admin callers with `Can not control alt-bots with this command.`
