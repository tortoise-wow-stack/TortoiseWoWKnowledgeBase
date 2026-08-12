---
type: Guide
title: Tortoise WoW Knowledge
description: Repository entry point for the deployment-agnostic Tortoise WoW knowledge bundle.
tags: [guide, repository]
status: stable
---

A deployment-agnostic knowledge bundle for operating and modifying a solo Turtle WoW 1.18.1 server with the Tortoise core and PlayerBots.

Start with:

- [Agent guide](AGENTS.md) for task routing and safety boundaries
- [Knowledge index](index.md) for the complete topic listing
- [PlayerBots capability map](playerbots/capability-map.md) for source-pinned bot behavior and commands

The bundle intentionally excludes hostnames, endpoints, SSH aliases, accounts, credentials, character names, live settings, and other deployment-specific values. Supply those through a separately protected private deployment record when performing operational work.

## Validation

```bash
python3 tools/validate_shareability.py
python3 tools/validate_playerbots_docs.py
```
