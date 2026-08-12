---
type: Reference
title: PlayerBots LLM & chat systems
description: The bot chat pipeline — scripted texts, broadcasts, speak/talk/say commands — and the LLM roleplay integration (plumbed but stubbed at the network layer).
tags: ["playerbots", "chat", "llm"]
resource: https://github.com/Shyalya/tortoise-wow/tree/playerbots-integration-gh/src/modules/PlayerBots/playerbot
status: stable
generated: { by: pi/agent, at: 2026-08-11T17:10:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---

# PlayerBots LLM & chat systems

**Related:** [PlayerBots command reference](/playerbots/commands.md) · [PlayerBots modification](/playerbots/modification.md) · [PlayerBots behavior systems](/playerbots/behavior-systems.md)

## Scripted chat (works today)

- **`say <name>`** — random line from `ai_playerbot_texts` (uniform random among same-name entries, locale-aware), chance-gated by `ai_playerbot_texts_chance` (taunt 30, aoe 75, loot 20); `/y` prefix → yell.
- **`speak <text>`** — says the argument verbatim; `/y /p /r /g /s /1..4` prefixes route the channel. **`talk`** = just the talk emote animation. **`chat`** = switches the bot's chat-channel mode.
- **Placeholders**: `%item_link`, `%area_name`, `%zone_name`, `%my_class`, `%rand1..3` … replaced sequentially (BOT_TEXT2).
- **Broadcasts**: per-channel chance pairs (guild/world/general/trade/LFG/local+world defense/recruitment/say/yell/city) × global chance (0–30000); lines from `ai_playerbot_texts` by event (`broadcast_looting_item_<quality>`, `broadcast_quest_accepted_generic`…).
- **`debug logname`** — per-bot CSV of everything the bot says (`chat_log_<botname>.csv`).

## LLM roleplay chat (plumbed, but STUBBED in this fork)

The whole pipeline exists: `ChatReplyAction::ChatReplyDo` intercepts whispers/say/yell/party/guild/channel when `llmEnabled > 0` + the `ai chat` strategy is active and the channel isn't blocked; builds per-channel context memory (placeholders: sender/bot name, gender, level, class, race, faction, zone, channel, message), appends the character-card persona, JSON-sanitizes, runs `Generate` async, parses with 4 regexes, and sends delayed chat/emote packets. `debug llm` echoes the JSON/parse stages. Bot-to-bot speech is LLM-gated too.

**BUT `PlayerbotLLMInterface::Generate()` is a stub in this fork**: *"LLM gateway network client removed. Always report no response"* — returns `{}`. So `ai chat` bots silently no-op; the raw BSD-socket+OpenSSL client is dead code (nothing calls it). A re-enabled backend could use `src/shared/httplib.h`.

**Config keys** (all in `aiplayerbot.conf`): `LLMEnabled` (default 1: 0 off, 1 on with `ai chat` strategy, 2 = `ai chat` default for all, 3 = always), `LLMApiEndpoint` (default `http://127.0.0.1:5001/api/v1/generate` — text-generation-webui; OpenAI-compatible `/v1/chat/completions` documented in conf), `LLMApiKey`, `LLMApiJson` (prompt template with `<pre prompt>/<context>/<prompt>/<post prompt>` slots), `LLMContextLength` 4096, `LLMGenerationTimeout` 600, `LLMMaxSimultaniousGenerations` 100, `LLMPrePrompt/Prompt/PostPrompt/RpgPrompt` (roleplay templates), 4 response regexes, `LLMGlobalContext`, `LLMBotToBotChatChance` 0, `LLMRpgAIChatChance` 100 (unused), `LLMBlockedReplyChannels`, `LLMDefaultPromptsFile = llm_character_card.txt`.

**Character card** (`llm_character_card.txt` — NOT in the repo; expected in the server root, parsed at startup): one `CharacterName::personality text` per line; the name must exist in the characters DB; the persona is stored per-bot in `ai_playerbot_db_store` and appended to the pre-prompt.

**To re-enable LLM chat:** implement `Generate()` (httplib or raw sockets) against a local LLM (e.g. llama.cpp/OpenAI-compatible on 127.0.0.1), create the character card, set `LLMEnabled` — the rest of the pipeline is complete.
