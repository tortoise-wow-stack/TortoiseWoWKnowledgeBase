---
type: Guide
title: Server rate tuning and validation
description: How to adjust Tortoise WoW rate families, understand their interactions, and verify changes without assuming a specific play style.
tags: ["tuning", "rates", "config", "validation"]
resource: file:///opt/turtle/etc/mangosd.conf
status: stable
generated: { by: pi/agent, at: 2026-08-16T00:00:00Z }
sources:
  - id: rates
    resource: /tuning/rates-limits.md
    title: Server rates & limits
  - id: config
    resource: /tuning/config-families.md
    title: Config families
  - id: env
    resource: /tuning/env-config.md
    title: Env-driven config
  - id: quests
    resource: /content-creation/quests.md
    title: Quest XP and rewards
  - id: factions
    resource: /content-creation/factions-professions.md
    title: Reputation and professions
  - id: instances
    resource: /content-creation/instances-bosses.md
    title: Instances and AutoScaler
  - id: bots
    resource: /playerbots/config.md
    title: PlayerBots config
  - id: persistence
    resource: /ops/persistence.md
    title: Persistence map
  - id: reloads
    resource: /ops/reloads.md
    title: Hot-reload commands
---

**Related:** [Server rates & limits](/tuning/rates-limits.md) · [Config families](/tuning/config-families.md) · [Env-driven config](/tuning/env-config.md) · [Change workflow](/workflows/change-playbook.md) · [Persistence map](/ops/persistence.md)

## Scope

Use this guide for any server-rate change: XP, rested progression, reputation, honor, drops, money, skills, talents, combat recovery, creature difficulty, auction behavior, or related limits. It is deployment-agnostic and describes a method for making intentional changes; it is not a live configuration snapshot or a required play-style profile.

Verify every key against the pinned image's `mangosd.conf.dist`, the current rendered configuration, and the relevant source-pinned documentation before changing it. Runtime facts and deployment paths belong in the private deployment record.

## Choose the correct rate family

Start with the narrowest family that matches the desired outcome:

| Desired outcome | Primary settings | Important boundary |
| --- | --- | --- |
| Leveling speed | `Rate.XP.Kill`, `.Quest`, `.Explore`, and separately `Rate.Rest.*` | These are separate XP sources; rested XP and character challenges can alter observed results. |
| Reputation or PvP progression | `Rate.Reputation.Gain`, `Rate.Honor`, `BattleGround.Rate.*` | Reputation also has DB source rates; honor and reputation are not XP. |
| Item or currency supply | `Rate.Drop.Item.*`, `Rate.Drop.Money` | Loot tables, quest rewards, vendor prices, and instance money can be separate inputs. |
| Talent and profession progression | `Rate.Talent`, `Rate.Skill.Discovery`, `SkillGain.*`, `AlwaysMaxSkillForLevel` | These do not increase level XP; PlayerBot premade talent data must match `Rate.Talent`. |
| Combat difficulty or recovery | `Rate.Creature.*`, `Rate.Health`, `Rate.Mana`, `Rate.Rage.Income`, `Rate.Energy`, `Rate.Focus` | These change the encounter or resource loop, not the reward multiplier. |
| Auction, corpse, or group convenience | `Rate.Auction.*`, `Rate.Corpse.Decay.Looted`, `MaxGroupXPDistance`, death/logout limits | These affect timing, eligibility, or convenience rather than base rewards. |

The full inventory and audited baseline values are in [Server rates & limits](/tuning/rates-limits.md:24). Other progression, operations, visibility, and security families are summarized in [Config families](/tuning/config-families.md:21).

## Example: changing base XP to 2x

If the intent is 2x for the three ordinary XP sources, change only these keys:

```ini
Rate.XP.Kill = 2
Rate.XP.Quest = 2
Rate.XP.Explore = 2
```

This is an example, not a universal recommendation. Setting only `Rate.XP.Kill = 2`, for example, intentionally leaves quest and exploration XP at their existing values. Leave `Rate.Rest.*` unchanged when first testing so the base multiplier is measurable.

“2x” here means 2x the selected base source. It does not guarantee 2x final XP in every situation: rested state, character challenges, XP toggles, level penalties, quest data, group eligibility, and bot-specific settings may also matter. The bundle documents the quest-XP formula more precisely than the kill, exploration, rested-XP, and challenge-ordering paths; verify those paths empirically against the pinned build.

## How rate changes interact

These are source-specific multipliers, not one global progression switch:

| Setting | Changes | Does not change directly |
| --- | --- | --- |
| `Rate.XP.Kill` | XP awarded for eligible creature kills | quest XP, exploration XP, reputation, loot, money, or combat difficulty |
| `Rate.XP.Quest` | The XP portion of quest rewards | the quest's `RewXP`, level-difference decay, quest reputation, item rewards, or max-level handling |
| `Rate.XP.Explore` | exploration/discovery XP | kill or quest XP |
| `Rate.Rest.*` | rested-XP accumulation | the base XP multiplier; rested characters can therefore appear to earn more than the base rate temporarily |
| `Rate.Reputation.Gain` / `Rate.Honor` | reputation or honor gains | any XP source |
| `Rate.Drop.*` / `Rate.Drop.Money` | item-drop chances or creature money | XP, reputation, or creature strength |
| `Rate.Talent` / `Rate.Skill.*` | talent points, recipe discovery, or skill progression | XP and level speed |
| `Rate.Creature.*` / `Rate.Health` / `Rate.Mana` / resource rates | creature difficulty or combat recovery | XP multipliers and reward tables |

For quests, the documented path is `RewXP × level-decay × Rate.XP.Quest`. A quest with `RewXP = 0` still awards no XP, and at the level cap the reward uses `RewMoneyMaxLevel` instead. `Progression.NoQuestXpToGold` is a separate max-level progression switch; verify its target-build behavior rather than treating it as another XP multiplier. See [quest rewards](</content-creation/quests.md:35>) and [quest XP](</content-creation/quests.md:39>).

Other systems can change what a player observes without changing the selected rate:

- Turtle character challenges such as War Mode and Slow & Steady have their own XP behavior; War Mode adds 20% XP and forces PvP, while the quest documentation says Slow & Steady skips the ordinary quest multiplier path. Challenges are selected at character creation. The player `xp` command can also toggle XP gain. See [Turtle systems](</tuning/turtle-systems.md:22>).
- `MaxGroupXPDistance` controls the range in which grouped players or bots can share XP; it does not multiply XP. Group composition and distance must be part of an XP test.
- PlayerBot `XPRate` is separate from the player's `Rate.XP.*` settings. The source-pinned notes describe a server-rate × `XPRate` relationship, but this bundle does not establish whether it applies identically to kill, quest, exploration, rested, group, or dungeon XP, or to every bot type. Verify the target build before changing it.

For the pinned PlayerBots baseline, `aiplayerbot.conf` states the relationship as:

```text
bot XP multiplier = server XP rate × AiPlayerbot.XPRate
```

This means a server-wide XP change can accelerate bots even when no bot setting is changed. If the intended effective bot multiplier is `B` and the relevant server multiplier is `S`, the compensating value is `AiPlayerbot.XPRate = B / S`; for example, preserving 3x bot progression while changing all three ordinary player XP sources to 2x uses `XPRate = 1.5`. This changes bot progression only; it does not change the real player's XP rate. Validate the target build's kill, quest, exploration, group, and dungeon paths before assuming the formula applies identically to every bot type or XP source. The distributed baseline contains `AiPlayerbot.XPRate = 3` despite an adjacent comment saying the default is 1, so use the rendered target configuration as the authority.

`reload config` rereads `mangosd.conf`; PlayerBots configuration has a separate GM-gated reload path. An in-container edit is temporary and is overwritten when the service is recreated unless the deployment persists `aiplayerbot.conf` through its supported configuration path.
- Quest completion can award XP and reputation together, but increasing XP does not increase the reputation part. Likewise, an XP change does not grant extra talent points or automatically keep weapon/profession skills current.

Related difficulty and convenience systems are not substitutes for rates. Leech, alive-on-repop, LFT bot fill, instance entry gates, and `AutoScalerEnable` change survivability, group formation, eligibility, or instance difficulty. AutoScaler can also generate scaled instance money loot, which is separate from `Rate.Drop.Money`; the bundle does not establish whether LFT bots count toward its player-count input. Test these systems independently from reward-rate changes.

## Important secondary effects

- A higher XP rate can make gear, money, reputation, and weapon/profession skills lag behind the character level even when their rates remain unchanged. Change those families only when the measured bottleneck is actually there.
- The audited baseline already records `Rate.Drop.Item.Uncommon = 2`; do not assume the economy starts at an all-ones profile.
- Leave `Rate.Talent = 1` unless talent pacing is an explicit goal. PlayerBot premade talent links are generated with a matching talent-rate parameter, so changing it requires regenerating and validating those links.
- Global creature HP/damage reductions compound with combat recovery, leech, bot groups, and instance scaling. They make content easier rather than making progression faster, and can alter money generation through faster kills.
- `Rate.Reputation.Gain`, DB `reputation_reward_rate`, and faction spillover are separate layers. A rate change cannot compensate for a disabled or missing DB reward source; see [factions and professions](/content-creation/factions-professions.md:29).

## Configuration and persistence layers

The same conceptual setting may have more than one operational layer:

| Layer | Use | Caution |
| --- | --- | --- |
| `mangosd.conf` | Core rates, limits, and server systems | Numeric keys not exposed by packaging need the supported generated-file or bind-mount path. |
| `aiplayerbot.conf` | Bot progression, timing, strategies, and population | Bot settings have separate reload and performance implications. |
| Private `.env` | Packaging-mapped overrides at container start | The current bundle documents selected mappings such as `LEECH_ENABLE`, `LFT_BOTFILL_ENABLE`, and `AI_*`; it does not imply that every numeric rate is env-mapped. |
| World/logon DB | Content, reward-source data, and persistent player state | Use the DB migration/reload workflow; do not replace a config-rate change with an untracked SQL edit. |

The console `reload config` command can reread `mangosd.conf`, but that is a runtime action, not a persistence mechanism. PlayerBot config reload is separately GM-gated. Raw edits inside a running container are diagnostic only and may be overwritten on recreation. See [hot reloads](/ops/reloads.md:20), [change workflow](/workflows/change-playbook.md:17), and [persistence](/ops/persistence.md:18).

## Safe change and validation workflow

1. Record the current image/source, rendered value, and intended outcome in the private deployment record.
2. Choose one rate family and change the narrowest set of keys that expresses the goal.
3. Validate the rendered Compose configuration without printing secrets.
4. Test the affected source in a controlled state: no rested bonus for base XP, known character challenge, known group distance, or a known loot/reputation/combat event as appropriate.
5. Check adjacent outputs separately so an existing override is not mistaken for an effect of the change.
6. Monitor current-process readiness, logs, CPU/memory/tick quality, and restart count after applying the supported deployment change.
7. Recreate the affected service again and verify that the intended value and behavior survive.

Useful test cases include:

- one kill, quest turn-in, and exploration reward independently for XP changes;
- rested and non-rested comparisons;
- grouped and out-of-range comparisons for group XP;
- a level-cap quest if quest-to-money behavior matters;
- loot, money, reputation, skills, and talents independently for reward/progression changes;
- an instance with and without AutoScaler when changing dungeon-related settings;
- bot progression and performance independently from player progression.

Restarts, configuration edits, SQL writes, image rebuilds, and deployment-specific commands require explicit owner approval and the private deployment record. Keep the last known-good configuration/image available for rollback.
