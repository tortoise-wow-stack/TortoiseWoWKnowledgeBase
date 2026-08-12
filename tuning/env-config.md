---
type: Reference
title: Env-driven config
description: The .env variables that override config keys at every container start.
tags: ["tuning", "env"]
resource: <private compose environment>
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
**Related:** [Persistence map](/ops/persistence.md) · [Server rates & limits](/tuning/rates-limits.md)

## §0 — What the private `.env` controls

These variables are packaging inputs, not suggested deployment values. Keep `.env` outside image build contexts and documentation. The current renderer interpolates database secrets into initialization SQL, so apostrophes are unsupported unless the renderer is fixed; generate distinct strong secrets within the accepted character set and test initialization without printing them.

| Env var | Config key | Typical (solo) |
| --- | --- | --- |
| `LOG_SQL` | LogSQL | 0 |
| `LEECH_ENABLE` | Leech.Enable | 1 |
| `SOLO_DUNGEON_REPOP_ALIVE_ENABLE` | SoloDungeonRepopAlive.Enable | 1 |
| `LFT_BOTFILL_ENABLE` | LFT.BotFill.Enable | 1 |
| `AI_PLAYERBOT_ENABLED` | AiPlayerbot.Enabled | 1 |
| `AI_MIN_RANDOM_BOTS` / `AI_MAX_RANDOM_BOTS` | AiPlayerbot.Min/MaxRandomBots | 10 / 10 |
| `WORLD_PORT`, `REALM_PORT`, `REALM_ID`, `REALM_ADDRESS`, `GAME_BIND_IP`, `DB_*`, `DATA_PATH`, `DATABASE_AUTOUPDATE_ENABLED` | ports / DB paths | — |
