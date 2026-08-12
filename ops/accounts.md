---
type: Reference
title: Accounts & permissions
description: Accounts, security levels (rank 0-6), how GM rights apply and refresh.
tags: ["ops", "accounts"]
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
**Related:** [GM command cheat-sheet](/tuning/gm-commands.md) · [Admin recipes via DB](/ops/admin-recipes.md)

## Accounts & permissions

Actual account names, credentials, and realm endpoints belong in the owner-supplied private deployment record. Keep credentials in a separately protected secret store rather than beside generally readable backups or documentation. The client must be build 7272 or newer for this fork's default login gate; set `realmlist.wtf` from the private endpoint record.

**Security levels (Tortoise deviates from stock cmangos):** 0=PLAYER, 1=OBSERVER, 2=MODERATOR, 3=DEVELOPER, 4=ADMINISTRATOR, 5=SIGMACHAD (anticheat only), 6=CONSOLE. There is **no SEC_GAMEMASTER**. The database column is `tw_logon.account.rank`. A session picks up a rank change only after a full logout to the login screen. Set it with `.account set gmlevel <account> <level>` in-game or through the server console.
