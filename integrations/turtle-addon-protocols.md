---
type: Reference
title: Turtle addon protocols (TW_ messages)
description: The addon-message surface the client addons use to talk to the server — LFG, shop, guild bank, transmog, titles and more.
tags: ["integrations", "addons", "protocols"]
resource: https://github.com/Shyalya/tortoise-wow/tree/playerbots-integration-gh/src/game
status: stable
generated: { by: pi/agent, at: 2026-08-11T18:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

# Turtle addon protocols (TW_ messages)

**Related:** [External integrations](/integrations/external-systems.md) · [Turtle systems](/tuning/turtle-systems.md) · [Client-side content](/client-side/dbc-mpq.md)

The Turtle client addons talk to the core through addon-channel messages with a `TW_` prefix, routed by `WorldSession::HandleTurtleAddonMessages` (ChatHandler.cpp). Prefixes found in the source:

| Prefix | System | Notes |
| --- | --- | --- |
| `TW_LFG` | Looking For Team (dungeon finder) | guild-chat protocol: rolecheck → queue → match → offers → teleport via `map_template` entrances; bot fill via LFTBotFill; HC players filtered |
| `TW_SHOP` | Donation shop | `BuyItem` flow, `Balance:` push to the addon; refunds |
| `TW_GUILDBANK` | Guild bank addon | HC-blocked except Infernal/HC60 |
| `TW_TRANSMOG` | Transmog | collection commands (`.tmogdelete`), cost/color logic in `feature_transmog` script |
| `TW_TITLES` | Titles | title UI |
| `TW_BUFF` | World buffs / buff UI | — |
| `TW_BGQ` | Battleground queue UI | — |
| `TW_CHAT` / `TW_D` | Chat / debug helpers | — |
| `TW_AVAILABLE` | Availability probe | addons probe the server for Turtle support |

**Implications for agents:** building a new client addon feature means speaking the same addon-message channel (`CMSG_MESSAGECHAT` addon type with `BOT\t`-style prefixing — see the bot module's own addon parsing) and handling it in `HandleTurtleAddonMessages`. The client requires `ALLOW_TURTLE_ADDONS=ON` (server embeds the Turtle addon public key, else "interface corrupt").
