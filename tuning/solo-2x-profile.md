---
type: Recipe
title: 2x XP and solo-play starter profile
description: A deployment-agnostic starting profile for a 2x base-XP personal Tortoise WoW server with PlayerBots and solo dungeon support.
tags: ["tuning", "solo", "xp", "playerbots"]
resource: file:///opt/turtle/etc/mangosd.conf
status: stable
generated: { by: pi/agent, at: 2026-08-16T00:00:00Z }
sources:
  - id: rates
    resource: /tuning/rates-limits.md
    title: Server rates & limits
  - id: env
    resource: /tuning/env-config.md
    title: Env-driven config
  - id: bots
    resource: /playerbots/config.md
    title: PlayerBots config
  - id: quests
    resource: /content-creation/quests.md
    title: Quest XP and rewards
  - id: turtle
    resource: /tuning/turtle-systems.md
    title: Turtle systems
  - id: instances
    resource: /content-creation/instances-bosses.md
    title: Instances and AutoScaler
  - id: persistence
    resource: /ops/persistence.md
    title: Persistence map
---

**Related:** [Server rates & limits](/tuning/rates-limits.md) · [Env-driven config](/tuning/env-config.md) · [PlayerBots config](/playerbots/config.md) · [PlayerBots performance](/playerbots/performance.md)

## Scope

This is a conservative starting point for a private, solo-oriented server. It is a recommendation, not a live-deployment snapshot. Verify every key against the pinned image's `mangosd.conf.dist` and the current rendered configuration before changing it. Turtle character challenges such as War Mode and Slow & Steady add separate XP modifiers, so this profile means **2x base server XP**, not necessarily 2x final XP for every character. The bundle documents the quest-XP formula more precisely than the kill, exploration, rested-XP, and challenge-ordering paths; verify those paths empirically against the pinned build.

## First-pass profile

Set the three ordinary XP sources to the same multiplier:

```ini
Rate.XP.Kill = 2
Rate.XP.Quest = 2
Rate.XP.Explore = 2
```

Leave rested-XP rates at `1` initially. Also leave reputation, money, item drops, creature health/damage, the level cap, starting level, and starting money unchanged until the base profile has been tested. This limits economy and difficulty changes while making leveling twice as fast. Review any existing non-default drop rate separately; the audited baseline includes `Rate.Drop.Item.Uncommon = 2`.

## How the rates interact

These are source-specific multipliers, not one global progression switch:

| Setting | Changes | Does not change directly |
| --- | --- | --- |
| `Rate.XP.Kill` | XP awarded for eligible creature kills | quest XP, exploration XP, reputation, loot, money, or combat difficulty |
| `Rate.XP.Quest` | The XP portion of quest rewards | the quest's `RewXP`, level-difference decay, quest reputation, item rewards, or max-level handling |
| `Rate.XP.Explore` | exploration/discovery XP | kill or quest XP |
| `Rate.Rest.*` | rested-XP accumulation | the base XP multiplier; rested characters can therefore appear to earn more than 2x temporarily |
| `Rate.Reputation.Gain` / `Rate.Honor` | reputation or honor gains | any XP source |
| `Rate.Drop.*` / `Rate.Drop.Money` | item-drop chances or creature money | XP, reputation, or creature strength |
| `Rate.Talent` / `Rate.Skill.*` | talent points, recipe discovery, or skill progression | XP and level speed |
| `Rate.Creature.*` / `Rate.Health` / `Rate.Mana` / resource rates | creature difficulty or combat recovery | XP multipliers and reward tables |

For quests, the documented path is `RewXP × level-decay × Rate.XP.Quest`. A quest with `RewXP = 0` still awards no XP, and at the level cap the reward uses `RewMoneyMaxLevel` instead. The `Progression.NoQuestXpToGold` setting is a separate max-level progression switch; verify its target-build behavior rather than treating it as another XP multiplier. See [quest XP](</content-creation/quests.md:35>) and [the full rate table](</tuning/rates-limits.md:26>).

The final observed XP can also be affected by character and group state:

- War Mode adds 20% XP and forces PvP; Slow & Steady applies its own XP rules and skips the ordinary quest multiplier path documented by this bundle. These challenges are selected when the character is created. The player `xp` command can also toggle XP gain. See [Turtle systems](</tuning/turtle-systems.md:22>).
- Hardcore is permadeath, while `SoloDungeonRepopAlive.Enable = 1` changes instance-death handling and LFT filters Hardcore players. Do not combine this starter profile with Hardcore until the pinned build's precedence is verified; the generic solo recommendations are not a Hardcore ruleset.
- `MaxGroupXPDistance` controls the range in which grouped players or bots can share XP; it does not multiply XP. LFT and bot-fill change who is in the group, so test with bots nearby and away.
- PlayerBot `XPRate` is separate from the player's `Rate.XP.*` settings. The source-pinned notes describe a server-rate × `XPRate` relationship, but this bundle does not establish whether it applies identically to kill, quest, exploration, rested, group, or dungeon XP, or to every bot type. Do not infer a universal 6x result from the shorthand; verify the exact target build before changing it.
- Quest completion can award XP and reputation together, but increasing XP does not increase the reputation part. Likewise, 2x XP does not grant extra talent points or automatically keep weapon/profession skills current.

Avoid stacking global creature-difficulty reductions with leech and instance scaling. Those settings make content easier rather than making progression faster, and they can also change the economy indirectly through faster kills or scaled instance money loot.

Enable the modest solo helpers:

```ini
Leech.Enable = 1
Leech.Amount = 0.05
SoloDungeonRepopAlive.Enable = 1
LFT.BotFill.Enable = 1
LFT.BotFill.DelaySeconds = 60
LFT.BotFill.LevelRangeBelow = 2
LFT.BotFill.LevelRangeAbove = 6
```

`Leech.Amount = 0.05` is the documented 5% PvE/solo/dungeon leech. `LFT.BotFill.*` requires the `TW_LFG` client addon. Keep these instance gates disabled unless there is a specific reason to change them:

```ini
Instance.IgnoreLevel = 0
Instance.IgnoreRaid = 0
```

When the packaging layer exposes these mappings, put the values in the private `.env` rather than editing the rendered file:

| `.env` variable | Rendered key |
| --- | --- |
| `LEECH_ENABLE=1` | `Leech.Enable` |
| `SOLO_DUNGEON_REPOP_ALIVE_ENABLE=1` | `SoloDungeonRepopAlive.Enable` |
| `LFT_BOTFILL_ENABLE=1` | `LFT.BotFill.Enable` |
| `AI_PLAYERBOT_ENABLED=1` | `AiPlayerbot.Enabled` |
| `AI_MIN_RANDOM_BOTS=10` / `AI_MAX_RANDOM_BOTS=10` | `AiPlayerbot.MinRandomBots` / `AiPlayerbot.MaxRandomBots` |

The `.env` names are packaging inputs, not universal core config keys. Confirm that the target Compose checkout supports each mapping before adding it.

Keep `AutoScalerEnable = 0` for the first pass. The fork documents linear instance HP/damage scaling by player count and group size, with a 5-man floor around 0.6 HP / 0.4 damage and additional 10/20/40-man clamps; it can also generate scaled instance money loot, which is separate from `Rate.Drop.Money`. The bundle does not establish whether LFT bots count toward the scaler's player-count input, so test the actual bot-filled party. Combining auto-scaling with bot groups, leech, and alive-on-repop can trivialize encounters.

## PlayerBots

If ambient bots are desired, begin with a small measured population rather than copying a hardware-independent ceiling:

```ini
AiPlayerbot.DisableActivityPriorities = 0
AiPlayerbot.RandomBotLoginWithPlayer = 1
```

When those keys are exposed by the deployment's packaging, `AI_MIN_RANDOM_BOTS=10` and `AI_MAX_RANDOM_BOTS=10` are a reasonable initial target. Increase in small steps only after checking world CPU, memory, tick quality, and restart count. Online active bots, not the size of the offline character pool, drive most of the cost.

Audit `AiPlayerbot.XPRate` after changing server XP. The documented behavior describes bot XP as the server rate multiplied by `XPRate`, but the exact source types and bot populations covered are not specified here. Treat `XPRate = 1` as a hypothesis for matching player progression, not a guaranteed formula, and verify it against the pinned build. Keep `AiPlayerbot.CommandServerPort = 0`, and review `BotCheats`/`RndBotCheats` for economy-breaking item or gold assistance.

## Optional second-stage QoL

Consider these only after the first pass is stable and the desired progression is clear:

- `AutoScalerEnable = 1` for under-filled instances.
- `AlwaysMaxSkillForLevel = 1` if weapon and defense skill catch-up is more valuable than the normal skill progression.
- `AllFlightPaths = 1` if travel convenience is preferred over exploration.
- A small reputation or money multiplier if solo repair and reputation costs are the actual bottleneck. Avoid changing loot and global creature difficulty as a first response.

Leave `Rate.Talent = 1` unless there is a specific reason to change talent pacing. PlayerBot premade talent links are generated with a matching talent-rate parameter, so changing `Rate.Talent` requires regenerating and validating those links as well.

Do not combine several difficulty-easing changes at once. Change one lever, test the affected gameplay path, and record the intentional override in the private deployment record.

## Suggested validation matrix

Test the base profile before adding optional modifiers:

1. With a new non-challenge character and no rested bonus, verify one kill, one quest turn-in, and one exploration reward independently.
2. Repeat one source while rested; compare the result separately from the base 2x check.
3. Test a grouped bot inside and outside `MaxGroupXPDistance`, then inspect bot and player level progression independently.
4. Run one bot-filled dungeon with `AutoScalerEnable = 0`; repeat with it enabled only if the first run is too difficult.
5. Check loot, money, reputation, skills, and talents separately so an existing override is not mistaken for an XP effect.
6. Test one quest at the level cap if max-level quest-to-money behavior matters.

## Persistence and verification

Environment-mapped toggles belong in the private `.env`; other `mangosd.conf` and `aiplayerbot.conf` values need the deployment's supported generated-file or bind-mount path. The console `reload config` command can reread `mangosd.conf`, but that is a runtime action, not a persistence mechanism, and it does not replace verification after recreation. PlayerBot config reload is separately GM-gated. Never rely on a raw edit inside a running container. After an approved change:

1. Validate the rendered Compose configuration without printing secrets.
2. Recreate only the affected `mangosd` service through the approved deployment workflow.
3. Require a readiness signal from the current process, then inspect the rendered non-secret values.
4. Test XP from kill, quest, and exploration sources, then test one bot-filled dungeon.
5. Recreate once more and verify that the intended values survive.

Restarts, configuration edits, SQL writes, image rebuilds, and deployment-specific commands require explicit owner approval and the private deployment record. See [Change workflow](/workflows/change-playbook.md) and [Persistence map](/ops/persistence.md).
