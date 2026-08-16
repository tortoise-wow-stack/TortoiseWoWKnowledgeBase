---
type: Playbook
title: Restoration and reverse-engineering workflow
description: Evidence-first workflow for reproducing Turtle WoW 1.18.1 behavior, including intentional quirks, before changing the Tortoise restoration fork.
tags: [workflows, restoration, reverse-engineering, validation]
status: draft
generated: { by: pi/agent, at: 2026-08-16T00:00:00Z }
sources:
  - id: penqle
    resource: https://github.com/Penqle/tortoise-wow
    title: Penqle/tortoise-wow restoration repository
  - id: maintainer-direction
    resource: <maintainer conversation supplied by the repository owner, 2026-08-16>
    title: Restoration scope, intentional-bug policy, and contribution expectations
---

**Related:** [Change workflow](/workflows/change-playbook.md) · [Conditional gossip](/content-creation/gossip-quests.md) · [DB migrations](/content-creation/db-migrations.md) · [Fork history](/references/fix-history.md)

## Restoration target

Penqle's fork is intended as a close restoration of the real Turtle WoW behavior, not a clean-room redesign of how content ought to work. A surprising behavior is therefore not automatically a defect. The target may intentionally retain an upstream bug, or approximate the data mistake that produced it, when evidence shows players experienced that behavior.

For example, a gameobject flag can appear technically necessary while evidence shows the live Turtle data omitted it. Preserving that omission may be the correct restoration outcome. The same rule applies to gossip: do not silently improve option visibility, repeatability, ordering, or quest credit beyond what the evidence supports.

Solo systems such as scaling and leech are historical additions from the repository's earlier personal-server phase. Their presence is not precedent for adding new convenience behavior to restoration content.

## Evidence ladder

Use the strongest evidence available and record conflicts:

1. Reproduce current behavior on the intended Turtle client/server version with a normal character in the exact quest state.
2. Capture observable facts: quest log before/after, NPC and option text, branch order, objective counters, repeat interaction, and reconnect persistence. Video or timestamped screenshots are preferable to memory.
3. Trace the Tortoise world data and core path at a pinned commit. Search migrations as well as base tables so later corrections are not mistaken for original state.
4. Compare related upstream commits, change records, and previous content patterns. Treat third-party database dumps and wiki descriptions as leads until corroborated.
5. If evidence is absent or contradictory, state the uncertainty and ask the maintainer before choosing the more polished behavior.

Never use a production deployment as the experimental database. Follow the [agent guide](/AGENTS.md): read-only inspection first, and obtain explicit owner approval for SQL writes, restarts, rebuilds, or other deployment changes.

## Work loop

1. **Scope one observable failure.** Identify zone, quest id/title, NPC or gameobject entry, character state, expected observation, and actual observation.
2. **Build the dependency map.** Trace relations, templates, objectives, gossip menus/options/text, conditions, scripts, and any C++ hook. For gossip, use the [conditional-gossip reference](/content-creation/gossip-quests.md).
3. **Form the smallest evidence-backed hypothesis.** Separate missing data, incorrect data, core behavior, and deliberate upstream quirk.
4. **Ship through a migration.** Keep base/fresh-install implications in view; do not rely on an unrecorded manual database edit.
5. **Test positive and negative states.** Include no quest, active quest, already-credited objective, ready to turn in, rewarded, wrong choice, repeat click, relog, and unrelated NPC services where applicable.
6. **Review the diff for restoration drift.** Remove speculative cleanup, unrelated formatting, commentary that merely restates the SQL, and changes not required by the captured behavior.
7. **Report compactly.** A useful PR states the reproduced failure, evidence, exact data path, why each changed row is necessary, and the in-game verification result.

## LLM-assisted contribution boundary

LLMs may accelerate source tracing and draft SQL, but the contributor remains responsible for understanding every row, testing it personally, and explaining it without generated filler. Warning signs called out by the maintainer include verbose, confident descriptions that obscure incorrect semantics and tiny changes surrounded by disproportionate comments.

Before submission, the contributor should be able to answer:

- Which runtime function consumes every changed column?
- Which character/quest states make each condition true or false?
- Which objective receives credit, by what command, and why is that command the correct one?
- What happens on a second click, after a relog, and after quest reward?
- Which observation proves the result matches Turtle rather than merely working?

Completion: the change reproduces the evidenced Turtle behavior, including evidenced quirks, on an isolated test database; the migration survives fresh install; and the PR is concise enough for a maintainer to audit row by row.
