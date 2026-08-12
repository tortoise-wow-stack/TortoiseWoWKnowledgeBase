---
type: Reference
title: Project history & design decisions
description: What this project is, where it came from, and why the deployment record is kept outside this shareable bundle.
tags: ["history"]
status: stable
generated: { by: pi/agent, at: 2026-08-11T17:40:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: original-project
    resource: https://github.com/Penqle/tortoise-wow
    title: Original Tortoise WoW repository
  - id: playerbots-fork
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW PlayerBots fork
---

**Related:** [Operational gotchas](/ops/gotchas.md) · [Community findings](/references/community-findings.md)

This bundle documents the lineage originating at [Penqle/tortoise-wow](https://github.com/Penqle/tortoise-wow) and the PlayerBots-enabled fork at [Shyalya/tortoise-wow](https://github.com/Shyalya/tortoise-wow). The PlayerBots behavior and command baseline is source-verified against the Shyalya fork; the upstream authors and contributors retain credit for the server implementation.

A concrete deployment should follow a phased plan—preflight audit, storage, matching client data, Compose configuration, disposable first boot, login/restart test, then verified backup—and keep its machine identities, endpoints, accounts, image digests, incident history, and acceptance evidence in an owner-supplied private deployment record outside this shareable bundle.

Design decisions worth knowing (all generic):

- **Image portability is evidence-based** — test a prebuilt image on the target CPU. Treat `SIGILL` as a compatibility symptom with an initially unknown cause; preserve diagnostics and use a reproducible local build as fallback rather than asserting a universal CPU requirement.
- **Fail-closed automation** — extraction or migration handoffs validate independent postconditions before promoting state. The fork's possible nonzero `MoveMapGen` completion code is acceptable only after semantic completeness checks, required GameObject navmeshes, and absence of failure lines.
- **Config persistence is layered** — `.env` for the render-mapped keys, bind-mount for everything else; see the persistence map.
- **PlayerBots are the ike3/cmangos line** — most AzerothCore-module advice does not apply; see the playerbots group.
