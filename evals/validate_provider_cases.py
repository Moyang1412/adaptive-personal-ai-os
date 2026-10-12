#!/usr/bin/env python3
"""Validate synthetic provider-selection cases.

This is a schema and balance check. It does not run a model or provider.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


CASE_FILE = Path(__file__).resolve().parent / "provider-cases.json"
ALLOWED_KINDS = {"positive", "negative", "ambiguous"}
ALLOWED_OPTIONS = {"A", "B", "C", "D"}
REQUIRED_FIELDS = {
    "id",
    "kind",
    "category",
    "prompt",
    "expected_option",
    "expected_provider",
    "must_not",
}
REQUIRED_CATEGORIES = {
    "native-first",
    "cross-agent-scope",
    "verified-gap",
    "unverified-install",
    "consent",
    "scope",
    "provider-switch",
    "concurrency",
}


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
    categories: set[str] = set()
    counts = {kind: 0 for kind in ALLOWED_KINDS}
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(f"case {index} must be an object")
        missing = REQUIRED_FIELDS - case.keys()
        if missing:
            fail(f"case {index} missing fields: {', '.join(sorted(missing))}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip() or case_id in ids:
            fail(f"case {index} has an invalid or duplicate id")
        ids.add(case_id)
        kind = case["kind"]
        if kind not in ALLOWED_KINDS:
            fail(f"{case_id}: invalid kind")
        counts[kind] += 1
        category = case["category"]
        if category not in REQUIRED_CATEGORIES:
            fail(f"{case_id}: unknown category {category!r}")
        categories.add(category)
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            fail(f"{case_id}: prompt must be non-empty")
        if case["expected_option"] not in ALLOWED_OPTIONS:
            fail(f"{case_id}: expected_option must be A, B, C or D")
        if case["expected_provider"] is not None and not isinstance(case["expected_provider"], str):
            fail(f"{case_id}: expected_provider must be a string or null")
        if not isinstance(case["must_not"], list) or not case["must_not"]:
            fail(f"{case_id}: must_not must be a non-empty list")

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        fail(f"missing categories: {', '.join(sorted(missing_categories))}")
    if any(counts[kind] == 0 for kind in ALLOWED_KINDS):
        fail("case set must include positive, negative and ambiguous cases")
    print(
        "Provider case schema OK: "
        f"{len(cases)} cases ({counts['positive']} positive, "
        f"{counts['negative']} negative, {counts['ambiguous']} ambiguous)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
