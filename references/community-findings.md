---
type: Reference
title: Community findings
description: "Web research: lineage, fork history, solo-play advice, gotchas from the community."
tags: ["references", "community"]
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
**Related:** [Turtle systems](/tuning/turtle-systems.md) · [Operational gotchas](/ops/gotchas.md)

## §7 — Web/community findings

- **Lineage:** this fork (Shyalya/tortoise-wow) is a **mangos-zero core** with the **ike3/cmangos PlayerBots line** (`aiplayerbot.conf`, `.bot add`, `RNDBOT` accounts). Advice for the AzerothCore `playerbots.conf`/`addclass` module does NOT apply.
- Solo systems ship **off** upstream: `AutoScalerEnable` (off by default; 1 = instance HP/DMG scaling, `ScalarMin5ManHP 0.6` / `ScalarMin5ManDMG 0.4`, 10-man 0.3, 20-man 0.1, 40-man 0.01), `Leech.*`, `SoloDungeonRepopAlive.*`, `LFT.BotFill.*` — commonly enabled for solo play.
- Fork author recommends starting with **`.bot add <name>` single-bot alts** over big random-bot pools; stock dist ships 1000/1000 bots — start small (10–50) for solo.
- XP rate is **config-only** in stock mangos (`Rate.XP.*`); this fork additionally has `.modify xp` (verified in source) for on-the-fly grants.
- LFT is a **client addon** (queue/role window; does not teleport you); alternative addon: AutoLFM (auto-invite keywords).
- Known fork history (all fixed here, useful context): premade specs are hand-built for Turtle's reworked trees + `Rate.Talent=1`; druid bear-form backfill; healer range 3×; BG mutex; bot-name `%` in vfprintf; 105M trigger inits/hour.
- DB autoupdater caveat: safe only on DBs built through the updater; on restored dumps it can replay old migrations until a duplicate-key failure blocks startup — if a restore ever blocks at boot, check migrations history.
- Build flag `ALLOW_TURTLE_ADDONS=ON` is already on in the fork's Dockerfile — without it the 1.18.1 client crashes "interface corrupt".
- Sources: Shyalya/tortoise-wow README, Penqle/tortoise-wow `mangosd.conf.dist.in`, ike3 mangosbot docs, turtlecraft forum, dkpminus/mangos-gm-commands.
