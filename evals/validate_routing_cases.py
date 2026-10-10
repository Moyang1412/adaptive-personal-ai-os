#!/usr/bin/env python3
"""Validate the privacy-safe routing regression case file.

This is a structural check, not a model-quality benchmark. It catches malformed,
duplicated, or unbalanced cases before a maintainer runs the manual/model eval.
It uses only the Python standard library so contributors need no dependencies.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CASE_FILE = ROOT / "routing-cases.json"
ALLOWED_KINDS = {"positive", "negative", "ambiguous"}
ALLOWED_MODES = {
    "总台调度",
    "工程执行",
    "导师",
    "决策",
    "研究员",
    "复盘",
    "验证",
    "关系沟通",
    "健康照护",
    "写回状态",
    "specific-skill",
    "clarify-or-brief-answer",
}
REQUIRED_FIELDS = {"id", "kind", "prompt", "should_trigger", "expected_mode", "expected_behavior"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not CASE_FILE.exists():
        fail(f"missing {CASE_FILE}")

    try:
        payload = json.loads(CASE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")

    if payload.get("schema_version") != 1:
        fail("schema_version must be 1")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("cases must be a non-empty list")

    ids: set[str] = set()
    counts = {kind: 0 for kind in ALLOWED_KINDS}
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(f"case {index} must be an object")
        missing = REQUIRED_FIELDS - case.keys()
        if missing:
            fail(f"case {index} missing fields: {', '.join(sorted(missing))}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            fail(f"case {index} has an invalid id")
        if case_id in ids:
            fail(f"duplicate case id: {case_id}")
        ids.add(case_id)

        kind = case["kind"]
        if kind not in ALLOWED_KINDS:
            fail(f"{case_id}: kind must be one of {sorted(ALLOWED_KINDS)}")
        counts[kind] += 1
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            fail(f"{case_id}: prompt must be non-empty")
        if not isinstance(case["should_trigger"], bool):
            fail(f"{case_id}: should_trigger must be boolean")
        if case["expected_mode"] not in ALLOWED_MODES:
            fail(f"{case_id}: unknown expected_mode {case['expected_mode']!r}")
        if not isinstance(case["expected_behavior"], str) or not case["expected_behavior"].strip():
            fail(f"{case_id}: expected_behavior must be non-empty")
        if kind == "negative" and case["should_trigger"]:
            fail(f"{case_id}: negative case cannot expect a trigger")
        if kind == "positive" and not case["should_trigger"]:
            fail(f"{case_id}: positive case must expect a trigger")

    for kind in ("positive", "negative", "ambiguous"):
        if counts[kind] == 0:
            fail(f"case set must include at least one {kind} case")

    print(
        "Routing case schema OK: "
        f"{len(cases)} cases "
        f"({counts['positive']} positive, {counts['negative']} negative, {counts['ambiguous']} ambiguous)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
