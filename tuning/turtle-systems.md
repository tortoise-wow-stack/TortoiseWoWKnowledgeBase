---
type: Reference
title: Turtle systems
description: Challenges (Hardcore/War Mode/...), Glyphs, LFT, Transmog, AutoDonation, world buffs.
tags: ["tuning", "turtle"]
resource: file:///opt/turtle/etc/mangosd.conf
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
**Related:** [Server rates & limits](/tuning/rates-limits.md) · [Client-side content](/client-side/dbc-mpq.md)

## §11 — Turtle systems in this fork (what exists & how to turn on)

**Challenges — chosen at CHARACTER CREATION (no config, no adding later without recreating the char):** Slow & Steady (XP scaling), Exhaustion, **War Mode** (+20% XP, forced PvP), **Hardcore** (permadeath; HC-only quests, HC chat, `Hardcore.DiffProtection = 1100`, `Hardcore.Disable.Duel = 0`), Vagrant, Boring, Craftmaster, Lunatic, Brewmaster, Heroic. Spells 50000–57846; removable at the Glyph Master (lvl 60 / quest 55055).

**Content systems (NPC/addon-driven; inspect the pinned default and private deployment override):**

- **Glyphs**: Glyph Master NPCs + gossip UI (script `glyph_master`), cosmetic shapeshift glyphs (spells 53002–53029). No config.
- **LFT**: always-on manager + client addon (`TW_LFG` protocol); solo fill via `LFT.BotFill.*` (§1).
- **Transmog**: controlled by `Transmog.Enable`, required-item, and money-rate settings; NPC + addon (`TW_TRANSMOGRIFY`), `.tmogdelete`.
- **Shop**: donation shop (coins), `Shop.RefundWindow = 2592000`, glyph item 50745 blocks purchases; `.shop log|refund` (GM).
- **AutoDonationPoints**: configurable coins for online time, persisted in logon-DB `donation_point_progress`.
- **AutoWorldBuff**: configurable periodic Zandalar/Warchief/Rallying buffs, with zones derived from `area_template`.
- **BeginnersGuilds**: configurable first-login automatic guild invitation; guild IDs are content/deployment data and must be checked before enabling.
- **Guild bank addon**: `TW_GUILDBANK` protocol, HC-blocked; `GuildBank.NpcEntriesAlliance/Horde = 80917/80918`.
- **Misc**: shellcoins (`.shellcoin`), custom skins, Infernal/Inferno mode, salt-flats racer, Turtle cinematic, `cartographer`/`copy`/`queststatuses`/`hcchat`/`hcmessages` player commands, `spells_turtle.cpp` script pack.

**SEC_PLAYER Turtle commands:** `cartographer`, `copy`, `petname`, `xp` (toggle your XP), `radio`, `hcmessages`, `shellcoin`, `hcchat`, `queststatuses`, `bot`/`rndbot`.
