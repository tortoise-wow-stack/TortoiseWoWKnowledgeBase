---
type: Reference
title: Server console & server control
description: Console command set, pending_commands DB queue, server shutdown/restart.
tags: ["ops", "console"]
resource: file:///opt/turtle/run/mangosd.in
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
**Related:** [Hot-reload commands](/ops/reloads.md) · [Admin recipes via DB](/ops/admin-recipes.md)

## §8 — Server console (FIFO) & server control

Console = write a line into `/opt/turtle/run/mangosd.in` (FIFO) — runs with **SEC_CONSOLE (6, highest)**. Dot prefix optional on console. Key console commands:

- `account create <name> <pass>`, `account delete <name>` (console-only), `account set gmlevel <name> <0-5>` (rank 6 is the console execution context, not an assignable account rank), `account set password <name> <pw> <pw>`, `account twofa`
- `server shutdown <secs> [code]`, `server restart <secs> [code]`, `server idleshutdown|idlerestart <secs>`, `server shutdown cancel`, `server exit` (console-only), `server info`, `server resetallraids`
- `broadcast <text>` (world announce), `notify <text>` (popup), `saveall`, `kick <name> [force]`, `mute|unmute|pausingmute`
- `ban account|character|ip <name> <NdNhNm> <reason>`, `unban ...`, `banlist ...`
- `character deleted list|restore`, `character erase` (console-only), `character clean todelete|items`, `character itemlog`
- `guild create|delete|invite|uninvite|rank|rename|leader`, `instance listbinds|unbind|groupunbind|stats`
- `reset honor|level|spells|stats|talents` (`reset all spells|talents` = console-only), `pdump list|load|write`, `variable`, `wareffort`
- `quit`, `crash` (intentional segfault — console-only), `perf enable|intervalreport|resources|cpu|memory`
- **In-game-only** (rejected on console): `additem`, `learn`, `modify`, `npc`, `go`, `tele`, `levelup`, `god`, `summon`, `bank`, `maxskill`, `cooldown`, `respawn`, `waterwalk`, `explorecheat`, `taxicheat`, `xp`, `radio`, `bot`…
- **Console-only**: `account delete`, `character erase`, `character clean *`, `reset all *`, `server exit`, `quit`, `crash`

### pending_commands — DB-driven command queue (external admin hook)

Table in **tw_logon**: `pending_commands (id, realm_id, command varchar(250), run_at_time unixtime)`. mangosd polls every 60 s, executes due rows with full console rights, then deletes them. No in-repo producer — it exists for an external admin/web-shop panel (Turtle's original). Fire-and-forget, no feedback channel.

```sql
INSERT INTO pending_commands (realm_id, command, run_at_time)
VALUES (1, 'broadcast Server restarting in 5 minutes', UNIX_TIMESTAMP()),
       (1, 'server restart 300', UNIX_TIMESTAMP() + 60);
```
