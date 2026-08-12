---
type: Reference
title: Fork fix history & ecosystem
description: What the forks have already fixed (playerbots, class/spell, content), who maintains what, and the spell_mod technique for client-matching fixes.
tags: ["references", "forks", "history"]
status: stable
generated: { by: pi/agent, at: 2026-08-11T18:00:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh) README
  - id: penqle
    resource: https://github.com/Penqle/tortoise-wow
    title: Penqle/tortoise-wow (active restoration)
---

# Fork fix history & ecosystem

**Related:** [Community findings](/references/community-findings.md) · [Upstream resources](/references/upstream-resources.md)

## Ecosystem (who does what)

- **Shyalya/tortoise-wow** — our base: playerbots integration (r-o-sh's branch vendoring ike3), Turtle solo systems, world DB in repo. The playerbots fixes are listed in its README (BGs, druid forms, healer range, target-value crash, BG mutex, anticheat null pointer, dungeon-fill roles, spec-selection skew, strategy-rebuild 105M/h, custom::learned cache, vfprintf `%` abort).
- **Penqle/tortoise-wow** — the ACTIVE 1.18.1 restoration (daily commits, ~380 PRs): class/spell passes (hunter, rogue, warrior, mage...), content fixes (gameobjects, quests), solo additions (Autoscale, Leech, Additional Talent Points), Eluna planned, playerbots "basic". Target build 7272. Its methodology: apply spell fixes via **`spell_mod`** to keep `spell_template` matching client data ("that's not how it was in 1.17.1" caveat) — a useful technique for our own spell work.
- **faemwow/tortoise-wow** — mage talent pass source; Docker/Nix build support.
- **r-o-sh/tortoise-wow** — playerbots-integration origin branch.

## What's already fixed in Shyalya's playerbots (don't re-fix)

BG queue/enter/flag bugs; dungeon-finder bot fill (roles held, shamans off tank slot, respec on role mismatch); druid bear form at 10/16/40 + backfill; healer range 125y → sane; stealth target break; summon without meeting stone; group loot voting; **premade specs generated for `Rate.Talent=1`** (stock vanilla links fail Turtle's reworked trees); cached-target use-after-free; recursive_mutex BG queue; anticheat null pointer on bot sessions; asymmetric LFT level window; spec-selection weights; strategy rebuild batching; custom::learned DB cache; bot-name `%` abort.

## Class/spell fixes shipped in the base fork (context for new work)

Flurry charges; Shield Specialization rage-per-rank; Sweeping Strikes multiproc; Embrace of the Viper set bonuses; Wild Regeneration timing; Alterac item effects; disenchant ids restored (+3450 items); mage talent pass (from faemwow); `SPELL_AURA_MOD_MANA_GAIN_PERCENT` applied; creature damage/durability cast bug; Shatter crit bonus; Healing Touch dangling-pointer fix; guild-bank signed-money overflow.

## Content fixes shipped as migrations

Graveyards (Barrens, Arathi, dungeon sub-zones); 18 trainers + Survival artisan rank; Syndicate quartermaster stock; Hellador Swiftluck; guild-bank gossip trigger; PvP trinket no longer drops the flag. Manual extras in `sql/tools/` (see db-migrations).

## Implication for agents

Before writing a "fix", check: Shyalya README (base fixes), Penqle commit history (latest restoration state), and `sql/tools/` (known manual fixes). Prefer `spell_mod` over editing `spell_template` when the client data must stay authoritative.
