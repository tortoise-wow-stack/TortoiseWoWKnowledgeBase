---
type: Reference
title: Client-side content (DBC/MPQ)
description: Which client DBCs gate content, patch MPQ rules, tools, addons, Config.wtf.
tags: ["client", "dbc"]
resource: <client directory>
status: stable
generated: { by: pi/agent, at: 2026-08-11T15:30:00Z }
verified: { by: process:live-server-audit, at: 2026-08-11T12:00:00Z }
sources:
  - id: live-server
    resource: <live server, read-only access>
    title: Read-only audit of a live server (DB, configs, logs)
  - id: source
    resource: https://github.com/Shyalya/tortoise-wow
    title: Tortoise WoW source tree (playerbots-integration-gh)
---
**Related:** [Skills & talents](/tuning/skills-talents.md) · [Spells](/content-creation/spells.md)

## §20 — Client-side content (1.18.1) — what needs DBC/MPQ work

**What each client DBC gates:** `Spell.dbc` (names/tooltips/icons/visuals), `ItemDisplayInfo.dbc` (item model + bag icon; missing row = green/pink box), `Item.dbc` (class/subclass/quality/slot + display link; missing = "?" icon, equip bugs), `CreatureDisplayInfo.dbc` (NPC model), `Talent.dbc` (talent UI), `SkillLine.dbc` (skill pane names). Format: standard WDBC (20-byte header, fixed records, string block) — same from vanilla through WotLK, well documented.

**Extract server data from a matching client:**

1. Use the exact client build accepted by the target server and preserve the only source copy until login succeeds.
2. Build the matching source with extractor support.
3. Run `mapextractor`, `vmapextractor`, `vmap_assembler`, then `MoveMapGen` from the client directory, in that order.
4. Validate `dbc`, `maps`, `vmaps`, and `mmaps` semantically: expected map coverage, non-empty assembled VMAP/MMAP outputs, required GameObject navmeshes, and no failure lines.
5. This fork's silent `MoveMapGen` may return a nonzero completion code; accept it only when the independent completeness checks pass.
6. Mount the verified data read-only into the runtime and complete a login, movement, and restart-persistence test before deleting source or extraction artifacts.

Archive hashes, extracted file counts, storage paths, and capacities are deployment provenance and belong in the private deployment record.

**Patch MPQs — the way to add client content:**

- Load order: `base.MPQ` → `speech2` → `patch-2.MPQ` → `patch.MPQ` → stock data MPQs; numeric patches `patch-1..patch-9` then alphabetic `patch-A..patch-Z`; later = higher priority.
- **CRITICAL: the 1.12 loader only accepts SINGLE-character suffixes** — `patch-10.mpq` is silently rejected. Use an unused single letter (e.g. `patch-K.mpq`).
- Turtle launcher has a Mods tab to enable/disable them; Turtle updates can purge `Data/` — keep backups.

**Tools:** WDBX Editor (modern, full WDBC support, MPQ export — the one to use; also "WotLK Item Import" for the red "?" fix), MyDbcEditor (1.12, used in Turtle spell guides), WoW-Spell-Editor (vanilla spell.dbc), Taliis (Java). MPQ packing: Ladik's MPQ Editor / MyWarCraftStudio. Turtle DBC dumps: github.com/oplancelot/Turtle-WOW-DBC.

**Addons:** `ALLOW_TURTLE_ADDONS=ON` = the core embeds Turtle's addon public key (for `Turtle_General`/`Turtle_GroupUI`) — without it the client crashes "interface corrupt". Addons live in `Interface/AddOns/`, TOC `## Interface: 11200` (standard 1.12 numbering — any 1.12 addon loads). Known: pfQuest-turtle, LFT, pfUI-turtle, TurtleRP.

**realmlist.wtf:** only `set realmlist` matters; `set patchlist` is 2.1+ and does nothing on 1.12 (harmless). Config.wtf under Wine: `gxWindow "1"`, `gxMaximize`, `gxResolution`, `ffxGlow "0"` (crash source on Wine), `Sound_EnableHardware "0"`, `movie "0"` (skip intro), `profanityFilter "0"`.

**Server-side mirror caveat:** the CORE also loads its own DBC copies from the server `dbc/` folder at startup — client DBC additions (e.g. ItemDisplayInfo) should usually be mirrored server-side where the core reads them (check which DBCs the core actually loads — only 42; see §3).
