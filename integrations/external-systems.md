---
type: Reference
title: External integrations (API, Discord, shop, shellcoins)
description: The HTTP transfer API, Discord bot, donation-shop flow, shellcoin economy, pending_commands producer and 2FA — how external systems hook into the core.
tags: ["integrations", "api", "discord", "shop"]
resource: ssh://<server>
status: stable
generated: { by: pi/agent, at: 2026-08-11T16:45:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

**Related:** [Server console & server control](/ops/console.md) · [Accounts & permissions](/ops/accounts.md) · [Shop & Donation Points](/tuning/skills-talents.md)

## HTTP API server — character transfer only

`src/shared/HttpApi/` (httplib SSL server) + `src/game/HttpApi/`. **Exactly two POST endpoints**, both character-transfer: `/initiate-transfer` (pdump dump + shellcoin→gold + fashion-coin mail) and `/proceed-transfer` (pdump import, `shop_logs.guid` update). Auth: `X-API-Key` header vs `HttpApi.TransferKey` (default "Gheor"). Config: `HttpApi.Enable` (dist default 0), `HttpApi.BindIP` (127.0.0.1), `HttpApi.BindPort` (50000), certs `Api.CertificatePath`/`ApiPrivateKeyPath`. `stopapi` console command stops it. **Not a general web API.**

## Discord bot (compiled under USING_DISCORD_BOT)

Real dpp-based bot (all intents), not a webhook. Config key `DiscordBot.Token` starts it only when non-empty. Slash commands include `gm`, `logs`, `lookup` (GM-only), `twofactor` (TOTP secret + QR), and `login` (modal auth; 2FA check is stubbed). Some notification channel IDs are hardcoded in source; audit and replace them before enabling rather than publishing deployment identifiers. `discbot stop` stops it. The source reserves a service-account identity that is excluded from world buffs, donation points, and analysis; configure any actual identity privately.

## Donation shop flow (end-to-end)

1. External web panel credits `tw_logon.shop_coins` (MySQL **triggers** on insert/update/delete write `shop_diff` — its `query` column holds literal labels `INSERT/UPDATE/DELETE`, **not executable SQL**; nothing in the core reads shop_diff — pure audit trail).
2. In-game: player addon sends `TW_SHOP` messages → `ShopMgr::BuyItem` → balance check → `UPDATE shop_coins` + `INSERT shop_logs` → async `ShopSendItemTask` delivers the item; refund (`refunded=1`, coins restored) on failure.
3. Negative balance blocks login (`WOW_FAIL_NO_TIME`).
4. In-core refunds: egg token 92010, race-change appearance +160, level-60 Turtle-Mode reward +200 coins.
5. `AutoDonationPoints` (Enable=0): 1 point/hour online per real account, persisted in `donation_point_progress`, flushes to shop_coins every 5 min.
6. **`pending_commands` producer is external** (nothing in-repo writes it): an external panel can execute ANY console command on the realm with ≤1 min latency — effectively console access for the web panel.

## Shellcoins (item 81118)

NOT the donation currency — a dynamic-priced tradeable item: base 20 silver, `buy = (count+1)*20`, `sell = count*20` (count = total item 81118 across all chars). Price re-evaluated every 10 min, holders notified, history in `tw_char.logs_shellcoin` (time, count, price). `.shellcoin` player command shows prices. No config keys.

## TwoFA

`account twofa` (GM) → generates a 32-char TOTP secret into `account.security` (varchar) + `locked = 2` (FIXED_PIN). Login: classic-client PIN prompt; token validated via TOTP; success whitelists the IP in `account_twofactor_allowed` for 30 days. GM ranks / ALWAYS_ENFORCE force PIN. Discord `login` checks the same flags but its token verification is stubbed.
