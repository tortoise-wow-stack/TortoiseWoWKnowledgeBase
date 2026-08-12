#!/usr/bin/env python3
"""Generate source-pinned PlayerBots action and strategy name catalogs."""
from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
from pathlib import Path

CREATOR = re.compile(r'creators\["([^"]+)"\]')
STAMP = "2026-08-12T10:15:00Z"
CLASS_NAMES = {"deathknight", "druid", "hunter", "mage", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"}


def names(path: Path) -> list[str]:
    return CREATOR.findall(path.read_text(encoding="utf-8", errors="replace"))


def typed_creators(root: Path, object_type: str) -> dict[str, list[str]]:
    """Collect creator keys only inside NamedObjectContext<T> class bodies."""
    grouped: dict[str, list[str]] = defaultdict(list)
    declaration = re.compile(
        rf'class\s+[A-Za-z0-9_]+[^{{;]*?NamedObjectContext\s*<\s*{re.escape(object_type)}\s*>[^{{;]*\{{',
        re.S,
    )
    for path in sorted(root.rglob("*")):
        if path.suffix not in {".h", ".cpp"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in declaration.finditer(text):
            opening = match.end() - 1
            depth = 0
            closing = None
            for index in range(opening, len(text)):
                char = text[index]
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        closing = index + 1
                        break
            if closing is None:
                raise RuntimeError(f"Unbalanced class body in {path}")
            rel = path.relative_to(root)
            group = rel.parts[0] if rel.parts and rel.parts[0] in CLASS_NAMES else "shared"
            grouped[group].extend(CREATOR.findall(text[opening:closing]))
    return dict(grouped)


def frontmatter(title: str, description: str, tags: str, commit: str) -> str:
    resource = f"https://github.com/Shyalya/tortoise-wow/tree/{commit}/src/modules/PlayerBots/playerbot"
    return f'''---
type: Reference
title: {title}
description: "{description}"
tags: [{tags}]
resource: {resource}
status: stable
generated: {{ by: process:playerbots-catalog-generator, at: {STAMP} }}
verified: {{ by: process:source-audit, at: {STAMP} }}
sources:
  - id: source-commit
    resource: {resource}
    title: Tortoise WoW PlayerBots source at commit {commit}
---

'''


def bullets(values: list[str]) -> str:
    return "\n".join(f"* `{value}`" for value in sorted(set(values)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Shyalya/tortoise-wow checkout")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "playerbots")
    args = parser.parse_args()
    source = args.source.resolve()
    pb = source / "src/modules/PlayerBots/playerbot"
    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    if not pb.is_dir():
        raise SystemExit(f"PlayerBots source not found: {pb}")

    strategy_root = pb / "strategy"
    action_groups = typed_creators(strategy_root, "Action")
    action_union = sorted(set().union(*map(set, action_groups.values())))
    action_body = frontmatter(
        "PlayerBots public action catalog",
        "Generated exhaustive shared and class action registration names at the pinned source commit.",
        '"playerbots", "actions", "catalog", "generated"', commit,
    )
    action_body += "# Public action catalog\n\n"
    action_body += (
        f"Generated from every `NamedObjectContext<Action>` registration at `{commit}`. The source union contains **{len(action_union)} unique names**. "
        "A bot receives shared plus its class/build action contexts, not this entire union. Registration does not guarantee that an action is possible for every state, map, target, or build. "
        "`test` is compile-time conditional; expansion-specific actions are source-visible but may not compile into Classic. Invoke through `.bot do`, inline `do`, or the parsed command surfaces described in [actions/strategies](actions-strategies.md).\n\n"
    )
    action_body += "## Unique action names\n\n" + bullets(action_union) + "\n\n"
    action_body += "## Context membership\n\n"
    for label in sorted(action_groups, key=lambda item: (item != "shared", item)):
        values = action_groups[label]
        action_body += f"### {label} ({len(values)} registrations; {len(set(values))} unique)\n\n{bullets(values)}\n\n"
    (args.output / "action-catalog.md").write_text(action_body, encoding="utf-8")

    strategy_groups = typed_creators(strategy_root, "Strategy")
    # StrategyContext.h also defines sibling contexts that inherit StrategyContext
    # rather than NamedObjectContext<Strategy> directly (movement/assist/quest/fish).
    strategy_groups["shared"] = sorted(set(strategy_groups.get("shared", [])) | set(names(strategy_root / "StrategyContext.h")))
    all_strategies = sorted(set().union(*map(set, strategy_groups.values())))
    strategy_body = frontmatter(
        "PlayerBots strategy catalog",
        "Generated exhaustive generic and class strategy registration names at the pinned source commit.",
        '"playerbots", "strategies", "catalog", "generated"', commit,
    )
    strategy_body += "# Strategy catalog\n\n"
    strategy_body += (
        f"Generated from strategy creator registrations at `{commit}`. The scanned union contains **{len(all_strategies)} unique names**. "
        "Strategies are context-sensitive: a bot receives generic plus its class/build contexts, not this entire union. Unknown names can be silently ignored. "
        "Expansion-gated classes such as death knight are not available in the Classic build. Use [actions/strategies](actions-strategies.md) for mutation syntax and role caveats.\n\n"
    )
    strategy_body += "## Generic and shared registrations\n\n" + bullets(strategy_groups.get("shared", [])) + "\n\n"
    strategy_body += "## Class registrations\n\n"
    for label in sorted(k for k in strategy_groups if k != "shared"):
        values = strategy_groups[label]
        strategy_body += f"### {label} ({len(values)} registrations; {len(set(values))} unique)\n\n{bullets(values)}\n\n"
    (args.output / "strategy-catalog.md").write_text(strategy_body, encoding="utf-8")

    print(f"action catalog: {len(action_union)} unique names")
    print(f"strategy catalog: {len(all_strategies)} unique names across {len(strategy_groups)} contexts")


if __name__ == "__main__":
    main()
