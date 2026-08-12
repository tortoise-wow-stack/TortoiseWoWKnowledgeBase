#!/usr/bin/env python3
"""Fail when the shareable Markdown bundle contains deployment-specific identifiers."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "non-loopback IPv4 address",
        re.compile(r"(?<![\w.])(?!(?:127\.0\.0\.1)\b)(?:\d{1,3}\.){3}\d{1,3}(?![\w.])"),
    ),
    (
        "filesystem UUID",
        re.compile(
            r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
        ),
    ),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("user-specific home path", re.compile(r"/(?:home|Users)/[^\s/]+/")),
    ("deployment data path", re.compile(r"/(?:mnt|media)/[^\s`]+")),
    ("deployment checkout path", re.compile(r"/opt/tortoise-docker(?:/[^\s`]*)?")),
    ("host-local service path", re.compile(r"/usr/local/sbin/[^\s`]+")),
    ("host block-device identity", re.compile(r"/dev/(?:sd|vd|nvme)[^\s`]+")),
    ("private companion-file pointer", re.compile(r"tortoise-wow-deployment\.md")),
    ("live row-count snapshot", re.compile(r"\b(?:rows? live|live:\s*\d|current values?)\b", re.I)),
    ("private image digest", re.compile(r"sha256:[0-9a-fA-F]{64}\b")),
)


def main() -> int:
    findings: list[tuple[Path, int, str, str]] = []
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), 1):
            for label, pattern in RULES:
                if pattern.search(line):
                    findings.append((path.relative_to(ROOT), line_number, label, line.strip()))

    if findings:
        for path, line_number, label, line in findings:
            print(f"{path}:{line_number}: {label}: {line}")
        print(f"FAIL: {len(findings)} shareability finding(s)", file=sys.stderr)
        return 1

    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    print(f"PASS: {markdown_count} Markdown files contain no blocked deployment identifiers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
