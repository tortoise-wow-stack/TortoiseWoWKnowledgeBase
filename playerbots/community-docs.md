---
type: Reference
title: PlayerBots community documentation (ike3 line)
description: The canonical ike3 mangosbot docs, community settings for solo servers, known issues, and the cmangos-fork feature diff.
tags: ["playerbots", "community", "docs"]
resource: https://ike3.github.io/mangosbot-docs/
status: stable
generated: { by: pi/agent, at: 2026-08-11T17:50:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: ike3
    resource: https://ike3.github.io/mangosbot-docs/
    title: ike3 mangosbot documentation (12 pages)
  - id: cmangos
    resource: https://github.com/cmangos/playerbots
    title: cmangos/playerbots fork README + command list
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [PlayerBots in-game usage](/playerbots/in-game-usage.md) · [PlayerBots command reference](/playerbots/commands.md) · [PlayerBots behavior systems](/playerbots/behavior-systems.md)

## The ike3 docs (canonical for this line)

Documentation entry point: `ike3.github.io/mangosbot-docs/`. Key facts beyond the source extraction:

- **QuickStart**: `.bot add <name>` → bot appears nearby → invite → whisper `follow`. Bots mirror your quest accept/turn-in; `[quest]` link = status; `r [item]` = reward; `e [item]` = equip; trade window + `[item]` link or gold as `2g 3s 5c`; `trainer learn` at the class trainer.
- **Controlling**: bots obey their **master only**; master must be within control range (~100 yd); `do <action>` = one-shot, strategies = persistent; `co`/`nc`/`ds` with `+ - ~ ?` (the cmangos line renames `ds`→`de`); incompatible strategies auto-remove each other (stay vs follow).
- **Movement**: default state is `stay`; `follow` is instance- and taxi-aware; **meeting-stone summon needs no second player**; raw recipes: flee = `nc -stay,+follow,+passive` + `co +passive` + `do follow`.
- **Attacking**: bots never start combat unless attacked or told (exceptions: `grind`, `do attack`); tank = `tank assist`/`tank aoe`, DPS = `dps assist`/`dps aoe`, default `attack weak` (lowest HP); buffs `bdps/bspeed/bhealth/bmana`, resists `rfire/rfrost/rshadow/rnature`; add target-selection strategies to BOTH `co` and `nc`.
- **Looting**: `d loot`, `d add all loot`; `nc +loot` auto-loot (gather needs loot too); loot-list filters `ll gray|quest|skill|normat|all`, `ll [item]`/`ll -[item]`. Docs warn: keep auto-loot off, macro `d loot`.
- **Interacting**: `stats`, `quests` (+all/completed/incompleted/summary), `q [quest]`, `drop`, `accept [quest]`/`accept *`, `r [item]` (bots never self-pick rewards), `talk`.
- **ItemsAndTrading**: trade only with master; `[item]` = count/usefulness; `u [item] [target]`; `e`/`ue`; `s [item]`/`s *` (sell grays); `b`, `bank [item]`/`bank -[item]`, `gb [item]`/`gb -[item]`; NPC must be in direct contact.
- **Macro kit**: F=`/p follow`, G=`/p stay`, H=`/p flee`, Shift+T=`/p d attack my target`, T=`/p @tank d attack my target`, P=`/p co ~passive,?`, J=`/p d add all loot`; `/r` in raids.

## Community settings for small/solo servers

- Bot counts: ike3 docs say 100–200 random bots "need a relatively powerful server"; community consensus for small realms: **start 20–40 (recommended 25/25)**, raise by ~10 only if smooth.
- Starter block: `Enabled=1`, `RandomBotAutologin=1`, `Min/MaxRandomBots=25`, `MinLevel=1/MaxLevel=60`, `RandomBotJoinLfg=0` (solo — invites only), `SyncQuestWithPlayer=1`, `AutoLearnTrainerSpells=1`, `AutoLearnQuestSpells=1`.
- Timing (community example; verify units and key semantics against this fork before applying): `RandomBotUpdateInterval=60`, `RandomBotCountChangeMin/Max=1800/7200`, `Min/MaxRandomBotInWorldTime=3600/1209600`, `RandomBotRpgChance=0.20`, `RandomBotMaxLevelChance=0.15`, `ShowProgressBars=1`.
- First-launch character/gear generation is expensive — don't judge performance until after it finishes.

## Known issues & workarounds

- **Questing**: bots can fail to loot quest items / pick non-quest items (group loot rules matter; master loot can restrict bots) — known logic limitation (cmangos issue #3855).
- **Travel**: stuck bots across maps → meeting-stone summon (no 2nd player); reset with `follow` after removing `stay`/`passive`.
- **Performance**: monitor with `.rndbot diff` (avg/max server diff; **>150 ≈ lag**) and `.rndbot stats`.
- **BoostFollow** (cmangos line): bots speed up to stay close; disabling gives more separation but more terrain/boat/portal stucks.
- Don't mix in **Blueboy-line** docs (playerbot/mangos wiki) — different syntax.

## cmangos-fork feature diff (later line — may not exist in this port)

`.bot gear|upgrade|enchants|learn|train|pet|prepare|ammo|food|potions|reagents|consumables`, `talents` (named builds or raw WoWHead strings), `keep equip|greed|need`, `outfit` system, chat filters `@tank/@heal/@dps/@class/@group1-3/@1-10/@dead/@ranged/@melee`, `rti`/`rti cc`, `range <type> <amount>`, `wait for attack time <sec>`, `ss` spell blacklist, `autocast`, `ra`, `rtsc`, `go npc`/`go zone`, `.rndbot reload|diff|stats|teleport`. In this port, source-derived docs elsewhere in this bundle record `.bot init [white|green|blue|epic|legendary|sync]`; treat the `rare|uncommon` spelling as later-line documentation until source verification proves otherwise. `summon` semantics may differ (ike3 = summon to inn after `home`; cmangos = force-summon to you).
