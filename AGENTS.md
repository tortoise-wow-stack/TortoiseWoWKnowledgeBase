---
type: Agent Guide
title: Tortoise WoW server — agent guide
description: Task routing, operating boundaries, and critical invariants for agents working with this bundle.
tags: [agents, guide]
status: stable
generated: { by: pi/agent, at: 2026-08-12T10:15:00Z }
verified: { by: process:source-audit, at: 2026-08-12T10:15:00Z }
sources:
  - id: okf
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format v0.2 specification
  - id: bundle-audit
    resource: /log.md
    title: Bundle and live-server audit history
---

This directory is an OKF v0.2 knowledge bundle for a solo Turtle WoW 1.18.1 server (Tortoise core + PlayerBots). It is deployment-agnostic and shareable. Hostnames, addresses, SSH aliases, accounts, credentials, character names, device identities, capacities, co-tenants, live settings/counts, incident timelines, and deployment-specific host paths belong in an owner-supplied private deployment record outside this bundle. For deployment work, ask for that record and keep its values private.

Project intent: treat this bundle as offline preservation and research documentation for local, non-commercial use. Do not interpret it as authorization or instructions to operate a public service, expose a game server to the internet, monetize access, or imply affiliation with Blizzard Entertainment, Turtle WoW, or the upstream maintainers.

The PlayerBots capability baseline is pinned to source commit `172ee948e591f8bf1b53ea6389e3102186339f6e`; generated and source-verified at `2026-08-12T10:15:00Z`. Treat each concept's frontmatter independently. A `verified` event means that concept was checked against its named source; no `verified` key means unverified, not false. Runtime facts can change after verification, so re-check the live system before acting. Full listing: `index.md`; audit history: `log.md`. Internal links beginning with `/` are relative to this bundle root.

Read the file that matches the task — each is self-contained:

* **Check / restart / monitor a deployment** → obtain its private deployment record, then use `ops/access-status.md` + `ops/everyday-tasks.md`
* **Change server values (rates, limits, solo systems)** → `tuning/index.md`
* **Add or edit content (NPC, quest, item, spell, boss, event)** → `content-creation/index.md`
* **Work with bots (commands, config, modification)** → `playerbots/index.md` → `playerbots/capability-map.md`; exact command syntax is in `console-commands.md`, chat/`@` filters in `chat-surface.md` + `audience-filters.md`, addon integration in `addon-transport.md`, and ownership/failures in `security-failures.md`.
* **Admin actions via SQL or console** → `ops/admin-recipes.md`, `ops/console.md`, `ops/reloads.md`
* **External integrations (transfer API, Discord, donation shop, shellcoins, 2FA)** → `integrations/external-systems.md`
* **Housing & character services (rename/race/appearance tokens)** → `ops/housing-services.md`
* **Diagnose (logs, perf, crash recovery)** → `ops/logs-monitoring.md`
* **Client-side needs (DBC/MPQ patches, addons)** → `client-side/dbc-mpq.md`
* **Decide HOW to make a change (config vs SQL vs C++ vs client)** → `workflows/change-playbook.md`
* **Navigate the C++ source / find where code lives** → `references/codebase-map.md`
* **Ship SQL changes properly (migrations)** → `content-creation/db-migrations.md`
* **Know what's already fixed / who maintains what** → `references/fix-history.md`
* **Find official docs and tools** → `references/upstream-resources.md`
* **Speak the Turtle addon protocols (TW_ messages)** → `integrations/turtle-addon-protocols.md`
* **Understand the design and deployment history** → `history/implementation-plan.md`

Ground rules:

* **Live-system boundary:** begin with read-only inspection. Do not restart services, edit config, run SQL writes, rebuild images, or expose secrets without explicit owner approval. Use `sudo -n docker compose ...` when the deployment user is not in the Docker group.
* **Access discovery:** obtain the SSH method, endpoints, Compose directory, and privilege model from the owner-supplied private deployment record; never infer them from placeholders or examples in this bundle.
* **Health evidence:** a historical `World server is up and running` line is insufficient. Check current container state/restart count and require a readiness line emitted after the current container's `StartedAt`.
* Commands are verbatim templates; substitute deployment placeholders from private notes. Each operational task ends with a checkable completion condition.
* The `.env` + `docker compose up -d` path is the only supported config persistence; other options and their caveats are in `ops/persistence.md`.
* Never print `.env` secrets. Never reset the `db-data` and `init-marker` volumes separately — always together, and take a dump first.
* After SQL edits, prefer `.reload <table>` (list in `ops/reloads.md`); `faction`, `faction_template`, `skill_line_ability`, `spell_template` and `gameobject_template` need a core restart.
* The server console is the mangosd FIFO (`/opt/turtle/run/mangosd.in`) — write one command line per message, dot prefix optional.
* Client builds below 7272 are rejected at login. Image choice is deployment-specific: validate CPU compatibility, pin the tested image/source, and preserve a rollback image.
