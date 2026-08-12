---
type: Reference
title: Config families (the rest of mangosd.conf)
description: Source-configured families beyond rates; exact defaults and live values must be checked against the pinned image or deployment.
tags: ["tuning", "config"]
resource: file:///opt/turtle/etc/mangosd.conf
status: stable
generated: { by: pi/agent, at: 2026-08-11T17:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [Server rates & limits](/tuning/rates-limits.md) · [Turtle systems](/tuning/turtle-systems.md) · [Battlegrounds & PvP](/tuning/battlegrounds-pvp.md)

## Configuration families

The examples below describe keys present in the audited fork/image and illustrate their relationships; they are not a recommended profile or a statement about any live deployment. Check `mangosd.conf.dist` for the pinned source/image and inspect the rendered config privately before changing values.

- **Progression.\*** (Turtle era-gating): `ContentPhase = 3` (0–3; not 4), `RestoreDeletedItems = 1`, `AccuratePetStatistics/LFGAvailability/PVEEvents/SpellEffects = 1`, `NoRespecPriceDecay = 1`, `NoQuestXpToGold = 1`, `UnlinkedAuctionHouses = 1`.
- **GM.\*** (15): `LoginState = 1`, `StartLevel = 60`, `StartOnGMIsland = 1`, `InGMList.Level = 3`, `InWhoList.Level = 3`, `AcceptTickets = 1`, `AllowTrades = 1`, `JoinOppositeFactionChannels = 0`.
- **Log.\*** (~40): 17 `LogFilter_*` toggles, per-domain log files (`BgLogFile`, `GmLogFile`, `CharLogFile`, `HonorLogFile`, `RaidLogFile`, `ChatLogEnable = 1`, `LootsLogFile`, `LevelupLogFile`…), `LogMoneyTreshold = 10000`.
- **Chat / anti-spam**: `Chat.MinLevel = 1`, `ChatFlood.MessageCount = 10 / Delay = 1 / MuteTime = 10`, `Antiflood.Sanction = 4`, `ChatStrictLinkChecking.Severity = 2`, `WorldChan.MinLevel = 1`, `WhisperTargets.MaxTargets = 15 / DecayTime = 1800 / BypassLevel = 40`, `ListenRange.Say = 40 / Yell = 300`, `Channel.SilentlyGMJoin = 1`.
- **Server/ops**: `PlayerHardLimit = 4000`, `PlayerLimit = 0`, `LoginPerTick = 8`, `CharacterScreenMaxIdleTime = 900`, `CleanCharacterDB = 1`, `BackupCharacterInventory = 1`, `MaxPingTime = 30`, `BanListReloadTimer = 5`, `AsyncTasks.Threads = 2`, `UseProcessors = 0`, `ProcessPriority = 1`, `PidFile = "twlive.pid"`, `SaveRespawnTimeImmediately = 1`, `HttpApi.Enable = 0`, `Console.Enable = 1`, `PTR = 0`.
- **Combat/aggro**: `DebuffLimit = 40`, `ThreatRadius = 100`, `MaxCreaturesAttackRadius = 35`, `MaxCreaturesStealthDetectRange = 10`, `MaxCreatureSummonLimit = 100`, `CreatureFamilyAssistanceRadius = 10 / AssistanceDelay = 1500`, `EnvironmentalDamage.Min = 605 / Max = 610`, `Spells.CCDelay = 200`.
- **Corpse/Bones**: `Corpse.Decay.NORMAL = 300 / RARE = 900 / ELITE = 600 / RAREELITE = 1200 / WORLDBOSS = 3600` (seconds), `Bones.ExpireMinutes = 60`.
- **Items/Mail/Guild/Group**: `Item.InstantSaveQuality = 4`, `MailDeliveryDelay = 3600`, `MailMaxPerHour = 3`, `Mails.COD.ForceTag.MaxLevel = 61`, `MassMailer.SendPerTick = 10`, `Guild.EventLogRecordsCount = 100`, `Group.OfflineLeaderDelay = 300`.
- **Names**: `StrictPlayerNames = 1`, `MinPlayerName = 2`, `GameType = 6` (Turtle custom), `RealmZone = 1`, `DBC.Locale = 255`, `LoadLocales = 1`, `ActivateWeather = 1`, `ChangeWeatherInterval = 1200000`, `AddonChannel = 1`.
- **Perf/Movement/Visibility**: `Perf.Enable = 1`, `ReportInterval = 600`; `Visibility.Distance.BG = 533` / Continents & Instances 250, `ForceActiveObjects = 1`; `mmap.enabled = 1`, `MMapTileUnload = 0`; `Movement.ExtrapolatePlayerPosition = 0`, `MaxPointsPerPacket = 80`.
- **Anticheat/Suspicious**: master `Anticheat.Enable = 0` but ~77 per-check keys exist (ExploreArea/FlyHack/WallClimb/SpeedHack/Teleport…); `Suspicious.*` (Movement/Fishing/Npckilling) `Enable = 1`; `Warden.*` off.

## Audit before changing

Values in these families can affect progression, security, maintenance, networking, and performance simultaneously. Diff the rendered deployment config against the pinned image's `.conf.dist`, record intentional overrides in the private deployment record, and retest login, current-process readiness, and the affected gameplay path after a change.
