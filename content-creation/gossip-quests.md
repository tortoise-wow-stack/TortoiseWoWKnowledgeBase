---
type: Reference
title: Conditional gossip and quest credit
description: How data-driven gossip selects text, exposes options, follows branches, and grants quest-objective credit in this MaNGOS fork.
tags: [content, gossip, quests, conditions, db-scripts]
resource: mariadb://tw_world/gossip_menu
status: draft
generated: { by: pi/agent, at: 2026-08-16T00:00:00Z }
verified: { by: process:source-audit, at: 2026-08-16T00:00:00Z }
sources:
  - id: penqle-source
    resource: https://github.com/Penqle/tortoise-wow/tree/9f8335b2a0e87771e3af884449277633a961eddb
    title: Penqle/tortoise-wow source and world data at 9f8335b
  - id: maintainer-direction
    resource: <maintainer conversation supplied by the repository owner, 2026-08-16>
    title: Conditional-gossip restoration and review guidance
---

**Related:** [NPCs](/content-creation/npcs.md) · [Quests](/content-creation/quests.md) · [Conditions](/content-creation/conditions-areatriggers.md) · [Restoration workflow](/workflows/restoration-playbook.md) · [DB migrations](/content-creation/db-migrations.md)

## Mental model

Gossip is a runtime join across several systems rather than one self-contained table:

1. `creature_template.gossip_menu_id` selects the initial menu.
2. `gossip_menu` selects the page's `npc_text` and can start a `gossip_scripts` script. Multiple rows may share an `entry`; the core selects the qualifying row with the numerically highest `condition_id`.
3. `npc_text` selects up to eight `broadcast_text` records. The visible prose is stored in `broadcast_text` in this dataset.
4. `gossip_menu_option` supplies the clickable options. Its `condition_id` determines whether an option is present; `option_broadcast_text` takes precedence over fallback `option_text`.
5. Selecting an option may open another menu through `action_menu_id`, send a point of interest, invoke a service selected by `option_id`, and/or start `gossip_scripts` through `action_script_id`.

This explains the maintainer's shorthand: talk to NPC → menu → options and page text → `npc_text` → `broadcast_text`, with conditions and DB scripts layered over the path.

A legacy `npc_gossip` row can override the initial text for one creature spawn GUID. Check it when identical creature entries greet players differently; it is not a replacement for the entry-level branching in `gossip_menu`.

## Payment and combat branches

A gossip branch that mentions money still needs an executable payment path. `gossip_menu_option.box_money` is a schema field, but the deployed core does not retain it as an enforced runtime price; setting `box_money` alone therefore does not charge the player or make a complete payment flow.

Choose the seam deliberately:

* **Exact gossip UI:** in the maintained core extension, use a `SCRIPT_COMMAND_CREATE_ITEM` gossip action with `datalong = item_id`, `datalong2 = amount`, and optional `datalong3 = money cost in copper`; set `data_flags = 0x8` so failure aborts the script. The command validates money and inventory before deducting and creating the item. This is a source extension, not a portable assumption about every MaNGOS branch; verify the deployed `ScriptMgr.h`/`ScriptCommands.cpp` before authoring the SQL.
* **Vendor-backed, DB-only payment:** when that extension is unavailable, make the follow-up option `option_id = 3` (`GOSSIP_OPTION_VENDOR`), set its `npc_option_npcflag` to the vendor bit (`UNIT_NPC_FLAG_VENDOR = 128`), add the item to `npc_vendor`, set `item_template.buy_price` in copper, and put the quest gate on `npc_vendor.condition_id`. The normal vendor path checks the player's money and inventory before deducting the price and creating the item, but opens the vendor UI rather than a gossip confirmation.

Do not present `box_money` as a security check, and do not create the item before validating payment. A vendor price comes from `item_template.buy_price`, so changing an existing item changes its price everywhere it is sold. Use a dedicated item or a core-level payment seam when a global price change would be incorrect. Apply the quest condition at the purchase/action path as well as the visible option so a client cannot buy the quest item outside the intended state.

## Branching and side effects

For an ordinary talk option, `option_id = 1` (`GOSSIP_OPTION_GOSSIP`):

* `action_menu_id > 0` prepares and sends that next menu.
* `action_menu_id = 0` leaves the current interaction without opening a new page.
* `action_menu_id < 0` closes gossip and calls `TalkedToCreature` for the actual source creature.
* A nonzero `action_script_id` runs the matching rows in `gossip_scripts` after the option action. It can be combined with a next-page transition.

Do not confuse `gossip_menu.script_id` with `gossip_menu_option.action_script_id`: the former runs when the core chooses that page text; the latter runs when the player clicks that option.

For a combat response, use `action_menu_id = -1` to close the interaction and invoke `TalkedToCreature`, then attach a creature gossip script. Creature gossip scripts start with the NPC as source and the player as target, so `SCRIPT_COMMAND_SET_FACTION` can make the NPC temporarily hostile and `SCRIPT_COMMAND_ATTACK_START` can target the player. Change faction before starting the attack, use temporary-faction restore flags rather than a permanent template mutation, and give the attack command a later delay when the source must react to the new faction.

## One-time choices need durable state

`action_menu_id = -1` closes the current gossip window; it does not remember that a player made a choice. A one-time option therefore needs a persistent, player-specific marker and a condition that reads it.

A reusable item-marker pattern is:

1. Add a `CONDITION_ITEM` row (type `2`) for the marker item with flag `0x1` to require that the player **does not** have it. Use type `23` instead when the bank should count too.
2. Combine that condition with the active/incomplete quest condition using `CONDITION_AND` (type `-1`), whose values reference the two condition rows.
3. Attach the composite condition to the visible initial option, every follow-up option that must close after the choice, and the action script where the schema supports `gossip_scripts.condition_id`.
4. Confirm that every final branch creates or changes the marker. A branch with no durable state cannot be made one-time merely by closing the gossip window.

Test with a normal player by closing and reopening gossip, reconnecting, and retrying stale clicks. Failed payment or inventory validation must leave both the marker and the player's money unchanged.

## Conditions used by quest gossip

Both `gossip_menu.condition_id` and `gossip_menu_option.condition_id` refer to the shared `conditions` table. For quest conversations the common gates are:

* type `9` (`CONDITION_QUESTTAKEN`), `value1 = quest id`; `value2 = 1` means accepted and incomplete, while `2` means accepted and complete;
* type `8` (`CONDITION_QUESTREWARDED`) for already rewarded;
* type `19` (`CONDITION_QUESTAVAILABLE`) for currently eligible to accept;
* type `22` (`CONDITION_QUEST_NONE`) for neither accepted nor previously rewarded;
* flag `0x1` to reverse a condition result, and `0x2` to swap source and target.

There is no general per-objective-complete condition in this fork's `ConditionType`. A quest-active condition can hide an option before acceptance and after the whole quest completes, but does not by itself distinguish which one of several talk objectives has already received credit. Preserve the observed upstream behavior rather than inventing a per-player state mechanism without evidence.

Invalid condition references are neutralized during load after an error is logged, so a typo can expose content instead of safely hiding it. Validate every referenced condition and test as a non-GM character: GMs are deliberately shown condition-failing options with a marker.

Each `gossip_scripts` row may have its own `condition_id`. For creature gossip, the script begins with the NPC as source and player as target; DB-script target selection and `data_flags` can alter those objects before the row condition is evaluated. Do not copy a condition from a menu option into a script row without confirming its expected source and target.

## Quest-credit mechanisms

The DB-script command must match the objective representation in `quest_template`:

| Mechanism | Effect | Appropriate use |
| --- | --- | --- |
| `action_menu_id < 0` | Calls `TalkedToCreature` with the real gossip source entry | The objective directly names that NPC entry |
| command `83`, `SCRIPT_COMMAND_QUEST_CREDIT` | Calls `TalkedToCreature` with the DB-script source object's entry | The source entry itself is the talk objective |
| command `8`, `SCRIPT_COMMAND_KILL_CREDIT` | Grants credit for the creature entry in `datalong` | A talk interaction is represented by a dummy creature objective, including one objective among several |
| command `7`, `SCRIPT_COMMAND_QUEST_EXPLORED` | Calls `AreaExploredOrEventHappens` for the quest id in `datalong` | A whole exploration/event objective; the quest must carry special flag `0x002` |

Do not select a command from its name alone. Trace `ReqCreatureOrGOId1-4`, counts, objective text, and `SpecialFlags`, then confirm the same credit path on a test character.

## Common quest patterns

* **Investigation/interview:** each NPC option is gated to the active quest, opens its response page, and fires credit for one objective. When the quest uses dummy creature objectives, each option needs the matching explicit credit entry; merely opening the page does not progress the quest.
* **Quiz:** wrong answers normally branch to response text without credit, while the correct answer branches and fires a credit script. Test option ordering and repeat clicks rather than assuming the system tracks a per-player answered state.
* **Conversation-only objective:** a negative `action_menu_id` or command `83` may be enough when the real NPC entry is the objective. Do not add a dummy entry unless the source data and observed behavior require one.

Audit dummy objective identifiers against the complete world data before reusing them. A syntactically valid creature entry can already represent unrelated content, and fixing that collision speculatively can cause wider restoration drift.

Source anchors at the pinned commit: [`Player.cpp`](https://github.com/Penqle/tortoise-wow/blob/9f8335b2a0e87771e3af884449277633a961eddb/src/game/Objects/Player.cpp) for option filtering, page selection, branching, and script dispatch; [`Conditions.h`](https://github.com/Penqle/tortoise-wow/blob/9f8335b2a0e87771e3af884449277633a961eddb/src/game/Conditions.h) for condition semantics; and [`ScriptCommands.cpp`](https://github.com/Penqle/tortoise-wow/blob/9f8335b2a0e87771e3af884449277633a961eddb/src/game/Maps/ScriptCommands.cpp) for quest credit.

## Reload caveats

This source branch provides reload handlers for `conditions`, `creature_template`, `gossip_menu`, `gossip_menu_option`, `gossip_scripts`, `npc_gossip`, and `npc_text`. It has no separate `broadcast_text` reload command, so changing visible broadcast prose requires a broader supported reload path or restart. A `gossip_scripts` reload is refused while DB-script actions are scheduled because queued actions retain pointers to the loaded rows.

Reload availability is not authorization to mutate a deployment. Follow [AGENTS.md](/AGENTS.md), confirm the deployed source/schema instead of assuming this pinned Penqle branch, and obtain explicit owner approval before SQL writes or runtime reloads.

Treat gossip reloads as a dependency order: reload `conditions`, then `gossip_scripts`, then `gossip_menu_option`. If the option table is reloaded while its `action_script_id` is absent from the in-memory script table, the loader logs the missing script and drops that action for runtime; reloading the SQL row alone does not repair the already-loaded menu. If `gossip_scripts` reports that scripts are scheduled, wait for an idle window or use an approved restart before validating the branch. Vendor-backed payment changes also require the relevant `creature_template`, `npc_vendor`, and `item_template` reloads; test a fresh interaction after a template reload.

## Validation matrix

For each NPC/option, record the exact quest state and test at least:

| State | Expected observation to capture |
| --- | --- |
| Quest not accepted | Whether the quest-only option is absent |
| Quest active, objective not credited | Correct option, response page, and one credit event |
| Quest active, objective already credited | Whether the option remains, changes, or disappears; whether repeated clicks are harmless |
| All objectives complete but not rewarded | Completion text and absence/presence of investigation options |
| Quest rewarded | Default gossip restored; unrelated vendor/trainer/quest options unaffected |
| Paid branch (enough/insufficient money, full inventory, quest inactive) | No charge or item on failure; one item and one charge on success |

Use a normal player, not only a GM. Test wrong quiz answers as well as correct ones, reconnect between objectives, and verify the persisted quest counters. The completion condition is a concise migration whose every condition, branch, text, and credit row is traceable to captured behavior and survives a fresh database install.
