---
type: Reference
title: Server rates & limits
description: All Rate.* multipliers, limits and solo-play systems in mangosd.conf.
tags: ["tuning", "rates"]
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
**Related:** [Env-driven config](/tuning/env-config.md) · [Turtle systems](/tuning/turtle-systems.md)

## §1 — Server rates & limits (`mangosd.conf`)

File: `/opt/turtle/etc/mangosd.conf` in the container; template `mangosd.conf.dist` in the image. The table captures values from the audited source/image as a baseline, not a live deployment snapshot or a recommended solo profile. Re-check the pinned image before relying on any value.

**Rates:**

| Key | Default | Effect |
| --- | --- | --- |
| `Rate.XP.Kill` / `Rate.XP.Quest` / `Rate.XP.Explore` | 1 / 1 / 1 | XP multipliers |
| `Rate.Rest.InGame`, `Rate.Rest.Offline.InTavernOrCity`, `.InWilderness` | 1 / 1 / 1 | rested XP growth |
| `Rate.Reputation.Gain` | 1 | reputation multiplier |
| `Rate.Honor` | 1 | honor multiplier |
| `Rate.Drop.Item.Poor/.Normal/.Uncommon/.Rare/.Epic/.Legendary/.Artifact` | 1/1/**2**/1/1/1/1 | drop chance per quality |
| `Rate.Drop.Money` | 1 | money drops |
| `Rate.Talent` | 1 | talent points |
| `Rate.Skill.Discovery` | 1 | profession recipe discovery |
| `Rate.Health` / `Rate.Mana` / `Rate.Rage.Income` / `Rate.Energy` / `Rate.Focus` | 1 each | regen rates |
| `Rate.Creature.Aggro` | 1 | aggro radius (0 = never aggro) |
| `Rate.Creature.Normal/.Elite/.RARE/.RAREELITE/.WORLDBOSS` + `.Damage/.SpellDamage/.HP` | 1 each | per-tier creature difficulty (solo knobs) |
| `Rate.Auction.Time` / `.Deposit` / `.Cut` | 3 / 0 / 0 | AH speed & fees |
| `BattleGround.Rate.Honor.*`, `BattleGround.Rate.Reputation.*` | ~1 | BG multipliers |
| `Rate.Corpse.Decay.Looted` | 0.0 | corpse despawn after loot |

**Limits & QoL:**

| Key | Default | Effect |
| --- | --- | --- |
| `MaxPlayerLevel` | 60 | level cap |
| `StartPlayerLevel` / `StartPlayerMoney` | 1 / 0 | new character start |
| `AllFlightPaths` | 0 | 1 = all flight paths from the start |
| `AlwaysMaxSkillForLevel` | 0 | 1 = auto-max weapon/defense skill per level |
| `SkipCinematics` | 0 | 1 = skip intro cinematics |
| `CharactersPerAccount` / `.PerRealm` | 50 / 10 | character limits |
| `MaxPrimaryTradeSkill` | 2 | professions |
| `MinPetitionSigns` | 9 | guild creation |
| `MaxGroupXPDistance` | 74 | group XP range |
| `SkillChance.Orange/.Yellow/.Green/.Grey` | 100/75/25/0 | skill-up chance by color |
| `SkillGain.Crafting/.Defense/.Gathering/.Weapon` | 1 each | skill gain rates |
| `DurabilityLossChance.*` | 0.5/0.5/0.05/0.05 | durability wear |
| `Death.SicknessLevel` | 11 | res sickness from level 11 |
| `Death.CorpseReclaimDelay.PvP/.PvE` | 1 / 1 | 0 = instant reclaim |
| `InstantLogout` | 1 | instant logout |
| `CastUnstuck` | 1 | `.start` / unstuck |
| `AutoDonationPoints.Enable` | 0 | shop coins for online time |
| `Transmog.Enable` | 0 | transmog (ReqItemID 51217) |
| `AutoWorldBuff.Enable` | 0 | periodic world buffs |

**Solo-play systems (Tortoise additions):**

| Key | Default | Effect |
| --- | --- | --- |
| `Leech.Amount` | 0.05 | 5% damage leech (Leech.Enable=1, PvE/solo/dungeon-only) |
| `SoloDungeonRepopAlive.Enable` | 1 | death in an instance → respawn alive |
| `LFT.BotFill.DelaySeconds` / `.LevelRangeBelow` / `.Above` | 60 / 2 / 6 | dungeon queue bot fill |
| `AutoScalerEnable` | 0 | instance auto-scaling (0.6 HP / 0.4 DMG 5-man …) |
| `Instance.IgnoreLevel` / `.IgnoreRaid` | 0 / 0 | ignore instance entry requirements |
| `DynamicRespawn.*` | — | respawn scaling for low population |
| `WorldBossLevelDiff` | 3 | boss dynamic level |
| `AllowTwoSide.*` | 1 | cross-faction everything |
| `Anticheat.Enable` | 0 | off |
| `AutoRestart.MaxServerUptime` | 259200 | auto-restart every 3 days (04:00–06:00) |
