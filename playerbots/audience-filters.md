---
type: Reference
title: PlayerBots @ audience filters
description: "Complete source-verified leading @ filters for selecting bots before a chat command."
tags: ["playerbots", "chat", "filters"]
resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: source-commit
    resource: https://github.com/Shyalya/tortoise-wow/tree/172ee948e591f8bf1b53ea6389e3102186339f6e/src/modules/PlayerBots/playerbot
    title: Tortoise WoW PlayerBots source at commit 172ee948e591f8bf1b53ea6389e3102186339f6e
---


Filters are applied to each recipient's incoming command before trigger dispatch. A filter that does not match generally returns the original text (which means later composite passes may continue); a rejected filter returns empty and silently prevents that bot's command. Filters are not `.bot` target syntax and do not expose internal values as commands.

**Syntax:** place filters at the beginning, separated by spaces, followed by the ordinary chat command. Examples: `@tank do attack my target`, `@60 stats`, `@group2 follow`, `@quest=523 quests`, `@random=25 grind`.

## Complete filter families

| Family | Forms | Match |
| --- | --- | --- |
| Strategy state | `@nc=<strategy>`, `@nonc=<strategy>`, `@co=<strategy>`, `@noco=<strategy>`, `@react=<strategy>`, `@noreact=<strategy>`, `@dead=<strategy>`, `@nodead=<strategy>` | strategy present/absent in non-combat, combat, reaction, or dead engine |
| Role/range | `@tank`, `@dps`, `@heal`, `@notank`, `@nodps`, `@noheal`, `@ranged`, `@melee` | class/spec role and combat range; role tests are group-sensitive in RoleChatFilter |
| Level | `@<level>`, `@<low>-<high>` | exact level or inclusive range, e.g. `@60`, `@10-20` |
| Group | `@group`, `@group<N>`, `@group<N>-<M>`, `@nogroup`, `@leader`, `@raid`, `@noraid`, `@rleader` | party subgroup, ungrouped/group leader, raid membership/leader |
| Guild | `@guild`, `@guild=<prefix>`, `@noguild`, `@gleader`, `@rank=<prefix>` | guild membership/name prefix/leader/rank |
| Class | `@deathknight` (**WoTLK build only**), `@druid`, `@hunter`, `@mage`, `@paladin`, `@priest`, `@rogue`, `@shaman`, `@warlock`, `@warrior` | exact class |
| Race | `@<race-name>` | bot's formatted race name, lowercased first character; available races depend on build data |
| Raid target icon | `@star`, `@circle`, `@diamond`, `@triangle`, `@moon`, `@square`, `@cross`, `@skull` | bot is marked or current target is marked; requires a group |
| State | `@needrepair`, `@bagfull`, `@bagalmostfull`, `@outside`, `@inside` | durability/bag-space/overworld-instance state |
| Item usage | `@use=<item link>`, `@sell=<item link>`, `@need=<item link>`, `@greed=<item link>` | item-use classification; use item links, not arbitrary item IDs |
| Talent spec | `@<spec>` (for example `@frost`, `@holy`) | primary spec name from class/spec data |
| Location | `@<map-name>`, `@<zone-name>` | lowercased map or area/zone name |
| Probability | `@random`, `@random=<0-100>`, `@fixedrandom`, `@fixedrandom=<0-100>` | random 50% or requested percentage; fixed variant deterministically selects bot number |
| Quest | `@quest=<quest ID or quest link>` | bot has the current quest; IDs are extracted from link/text |
| Gear tier | `@tier<N>`, `@tier<N>-<M>` | source's gear-score bucket mapping, not a player level |

Filters can be chained, but composite passes and prefix parsing make malformed/ambiguous forms unsafe to treat as a stable grammar. Use a simple leading filter plus a simple command for addon macros. `@` filters are source-verified at `2026-08-12T10:15:00Z`; in-client behavior and local-language map/race/spec names need client verification.
