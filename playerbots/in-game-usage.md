---
type: Cheat Sheet
title: PlayerBots in-game usage
description: "Concise in-game routing for the source-pinned PlayerBots command baseline."
tags: ["playerbots", "commands"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


**Start here:** [capability map](capability-map.md). The detailed pages are [`.bot`/`.rndbot` commands](console-commands.md), [plain chat](chat-surface.md), [`@` filters](audience-filters.md), [actions/strategies/queries](actions-strategies.md), [addon transport](addon-transport.md), [security/failures](security-failures.md), [command config](command-config.md), and [offline vs random lifecycle](bot-lifecycle.md).

## Minimal syntax

* `.bot <command> [target] [parameters]` and `.rndbot <command> [target] [parameters]` are registered at `SEC_PLAYER`; `.ahbot` is a separate rank-2 command.
* Targets: current non-real-player bot, a name, comma-separated names, account-name expansion, `*` group, `guild`, or `!`. `!` is **rank 5+ / console only** in this port because the check is strictly above rank-4 `SEC_GAMEMASTER`; it is not ordinary GM+.
* `.bot group [size=N]` defaults to master plus four bots. `.bot create` accepts `name=`, `faction=`, `race=`, `class=`, `gender=`, `level=`, `role=tank|healer|dps`, `login=`, `group=`, `gear=`, `test=`, and `temporary=`.
* `.bot init [white|common|green|uncommon|blue|rare|epic|purple|legendary|yellow|sync]`; `.bot consums` aliases consumables. `.rndbot pid p i d` is a real command.
* `add/login` is asynchronous: `ok` means accepted, not necessarily in-world. `.bot do` is synchronous; `.bot cmd` is queued. `logout cancel` is supported. `queue` is not scheduled from whispers.

## Plain chat

No prefix is required by default. The exact 137 trigger keys, six alias families, channels/ranges, longest-prefix parsing, item-link behavior, inline `do`, `#` reply routing, silent failures, and delays are in [chat-surface](chat-surface.md). Leading `@` filters target role/level/group/guild/class/race/state/item/quest/location/probability/gear subsets; see [audience-filters](audience-filters.md).

`co +tank`, `co +heal`, and `co +dps` are **not universal roles**: only class contexts that register the placeholder accept those names; unknown strategy names can silently no-op. `ranged` is generic. `repop` is a `do` action (`do repop`), not a bare chat trigger.

## Solo/group flow

Use `.bot add <name>` for an owned alt or acquire a random bot through group/invite behavior. `.bot always <name>` is offline/free-alt AI and is distinct from a random-pool bot. Query addon state with an ordinary whisper `debug state` and consume the raw `CHAT_MSG_ADDON` response, or use TCP only when explicitly secured and configured; see [addon transport](addon-transport.md).

**Provenance:** source commit `172ee948e591f8bf1b53ea6389e3102186339f6e`; generated and source-verified `2026-08-12T10:15:00Z`. In-client delivery of addon-language packets remains unverified.
