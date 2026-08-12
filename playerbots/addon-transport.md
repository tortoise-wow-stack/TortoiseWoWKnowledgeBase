---
type: Reference
title: PlayerBots addon-facing transport and responses
description: "Source-verified chat and TCP transport behavior for addon authors, including request/response framing and security caveats."
tags: ["playerbots", "addon", "transport"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


## Recommended in-game path: whisper `debug <query>`

Send an ordinary plain-text whisper to the exact bot name, e.g. `debug state`. `PlayerbotAI::HandleCommand` executes the remote query synchronously and sends a server-built `CHAT_MSG_ADDON` packet to the requesting player. The packet contains the raw response as the message payload; this path does **not** prepend the normal addon prefix + tab format. An addon must therefore accept the raw response payload and correlate it by expected query/bot/time, not by addon prefix.

The debug branch occurs after the INVITE security gate but before the ALLOW_ALL gate. An ungrouped bot normally grants INVITE to strangers, so diagnostic queries may work for a stranger even though ordinary control commands do not. This is a source behavior, not an authorization recommendation. `CHAT_MSG_ADDON` sent *to* a bot is dropped, and ordinary `LANG_ADDON` text is dropped unless `BOT\t`-prefixed; `SendAddonMessage` cannot drive bot commands.

## `#a` reply override (compatibility path)

For ordinary command replies, `#w `, `#p `, `#r `, `#a `, and `#g ` set `currentChat` for three seconds. `#a` is parsed only with its trailing space. The reply implementation emits `BOT\t` + text as `CHAT_MSG_PARTY` with `LANG_ADDON`, not as a native addon-channel packet. Turtle client event routing for PARTY/LANG_ADDON must be verified in-client before relying on it. The incoming `BOT\t` convention is stripped by the server for compatibility.

## Optional TCP command server

When `AiPlayerbot.CommandServerPort` is nonzero **and** `AiPlayerbot.Enabled` + `AiPlayerbot.RandomBotAutologin` allow manager startup, the detached server binds `tcp::endpoint(tcp::v4(), port)`, i.e. all interfaces. There is no authentication, TLS, rate limit, or request-size bound in this source; each connection gets a thread and each newline-delimited request gets a newline-delimited response. This is a deployment/security risk: keep it disabled unless an owner explicitly controls network exposure.

Wire format:

```text
request:  <remote-command>,<random-bot-character-low-guid>\n
response: <remote-response>\n
```

A request without a comma returns `invalid request: <request>`. A GUID that is not an online random-pool bot with AI returns `invalid guid`. TCP reaches the random pool only; player-owned alt bots in a PlayerbotMgr are not reachable by GUID through this server. Remote responses are the exact query contracts in [actions/strategies](actions-strategies.md).

## Timing and correlation

TCP writes a response synchronously per request, but the handler runs through a detached connection thread and reads AI state without an explicit lock; clients should tolerate races. The chat debug packet is synchronous relative to input handling. Normal chat commands are queued for an AI tick (default `ReactDelay` 100 ms), while BOT_TEXT chatter can wait 10–20 seconds out of combat or 15–30 seconds in combat. `.rndbot stats` returns `Stats requested.` and prints later elsewhere; it is not an RPC payload. Add/login's `ok` means request accepted, not in-world readiness.

No secret, address, account, or deployment endpoint is part of this source baseline.
