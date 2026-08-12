---
type: Cheat Sheet
title: GM command cheat-sheet
description: In-game GM commands by purpose with security levels.
tags: ["tuning", "gm", "commands"]
resource: https://github.com/Shyalya/tortoise-wow
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
**Related:** [Accounts & permissions](/ops/accounts.md) · [PlayerBots in-game usage](/playerbots/in-game-usage.md)


## §4 — GM command cheat-sheet

**Items / gold / skills (rank 3):**

| Command | Example |
| --- | --- |
| `.additem` | `.additem 6948 20` (id or shift-click link; negative count removes) |
| `.additemset` / `.deleteitem` | set / removal |
| `.modify money` | `.modify money 100000` (copper; negative takes away) |
| `.maxskill` / `.setskill` | all skills / a specific one |
| `.learn` / `.unlearn` | `.learn 227` / `.learn all_myspells` |
| `.cooldown` | reset cooldowns |
| `.repairitems` / `.bank` / `.mailbox` | services |

**Level / XP / stats (rank 3; some rank 4):** `.levelup [N]`, `.modify xp`, `.xp on/off` (rank 0!), `.modify speed`, `.modify hp/mana/rage/energy/scale/morph`, `.modify strength/agility/stamina/...` (rank 4), `.reset talents` (3) / `.reset level/spells/stats/honor` (4), `.revive`, `.replenish`, `.die`, `.god`.

**Teleports (rank 1):** `.tele <name>`, `.go <name>`, `.go x y z [map]`, `.go corpse` (3), `.gps`, `.goname`, `.summon` (2), `.start` (3).

**Lookup (rank 2):** `.lookup item/quest/spell/creature/skill/itemset/object <fragment>` → IDs for `.additem` / `.learn` / `.npc add`.

**NPC / world (rank 3):** `.npc add <entry>`, `.npc delete`, `.npc spawn`, `.npc near/info/move`, `.npc set level`, `.respawn`, `.gobject add/delete/move/near`, `.waterwalk`, `.explorecheat`, `.taxicheat`.

**GM state (rank 2):** `.gm on/off`, `.gm visible`, `.commands` (list of commands you can use, rank 0).

**Radio (rank 0):** `.radio 1` (internet radio), `.radio 2` (local music — requires a companion music service; deployment notes describe the setup).

**Bots (rank 0):** `.bot <command> [botname]` — see §5.
