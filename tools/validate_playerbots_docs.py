#!/usr/bin/env python3
"""Validate OKF v0.2 structure, frontmatter, and Markdown links in this bundle."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
RESERVED = {"index.md", "log.md"}
STATUS = {"draft", "stable", "deprecated"}
ACTOR = re.compile(r"^(?:human:[^\s:]+|process:[^\s:]+|[^\s/:]+/[^\s/]+)$")
DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})$")


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    return yaml.safe_load(text[4:end]), text[end + 4 :]


def check_actor(value, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not ACTOR.fullmatch(value):
        errors.append(f"{where}: invalid actor {value!r}")


def main() -> int:
    errors: list[str] = []
    files = sorted(ROOT.rglob("*.md"))
    for path in files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        try:
            data, body = split_frontmatter(text)
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            data, body = None, text

        if path.name in RESERVED:
            if path.name == "index.md" and path == ROOT / "index.md":
                if data is not None and (not isinstance(data, dict) or set(data) != {"okf_version"}):
                    errors.append(f"{rel}: root index frontmatter may contain only okf_version")
            elif data is not None:
                errors.append(f"{rel}: reserved {path.name} must not have frontmatter")
            if path.name == "log.md":
                for line in body.splitlines():
                    if line.startswith("## "):
                        match = DATE_HEADING.fullmatch(line)
                        if not match:
                            errors.append(f"{rel}: invalid log date heading {line!r}")
                        else:
                            try:
                                date.fromisoformat(match.group(1))
                            except ValueError:
                                errors.append(f"{rel}: invalid calendar date {match.group(1)}")
        else:
            if not isinstance(data, dict):
                errors.append(f"{rel}: concept requires YAML mapping frontmatter")
                data = {}
            if not isinstance(data.get("type"), str) or not data["type"].strip():
                errors.append(f"{rel}: concept requires non-empty type")
            status = data.get("status")
            if status is not None and status not in STATUS:
                errors.append(f"{rel}: status must be draft, stable, or deprecated (got {status!r})")
            generated = data.get("generated")
            if generated is not None:
                if not isinstance(generated, dict) or "by" not in generated:
                    errors.append(f"{rel}: generated requires by")
                else:
                    check_actor(generated["by"], f"{rel}: generated.by", errors)
            verified = data.get("verified")
            if verified is not None:
                events = verified if isinstance(verified, list) else [verified]
                for index, event in enumerate(events):
                    if not isinstance(event, dict) or "by" not in event:
                        errors.append(f"{rel}: verified[{index}] requires by")
                    else:
                        check_actor(event["by"], f"{rel}: verified[{index}].by", errors)

        # Ignore Markdown-looking syntax inside inline/fenced code; C++ lambdas can contain [](...).
        scan = re.sub(r"```.*?```", "", body, flags=re.S)
        scan = re.sub(r"`[^`\n]*`", "", scan)
        for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", scan):
            target = match.group(1).strip().split("#", 1)[0].strip("<>")
            if not target or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target = target.split("?", 1)[0]
            resolved = (ROOT / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
            if target.endswith("/"):
                resolved /= "index.md"
            if not resolved.exists():
                errors.append(f"{rel}: missing link {target}")

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(files)} Markdown files; OKF structure, frontmatter, actors, lifecycle, and internal links valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
