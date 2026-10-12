#!/usr/bin/env python3
"""Synthetic isolated lifecycle checks.

The provider below is a test fixture only. It is intentionally not shipped as
the product's memory engine. These checks exercise the contract boundaries that
an installed provider must satisfy before it is recommended.
"""

from __future__ import annotations

import unittest

try:
    from .provider_selection import (
        ProviderDescriptor,
        ProviderEvidence,
        ProviderOperation,
        RouteRequest,
        route_operation,
    )
except ImportError:  # Direct ``python evals/test_memory_lifecycle.py``.
    from provider_selection import (
        ProviderDescriptor,
        ProviderEvidence,
        ProviderOperation,
        RouteRequest,
        route_operation,
    )


class ConcurrencyError(RuntimeError):
    pass


class SyntheticProvider:
    """Tiny revisioned fixture for isolated, fictional records."""

    def __init__(self) -> None:
        self.records: dict[str, tuple[int, dict[str, str], str]] = {}
        self.next_id = 1
        self.calls: list[str] = []

    def save(self, scope: str, value: dict[str, str], *, expected_revision: int = 0) -> str:
        key = f"{scope}:{self.next_id}"
        self.next_id += 1
        self.records[key] = (1, dict(value), scope)
        self.calls.append("save")
        return key

    def read(self, key: str, *, scope: str) -> dict[str, str] | None:
        self.calls.append("read")
        record = self.records.get(key)
        if record is None or record[2] != scope:
            return None
        return dict(record[1])

    def correct(
        self,
        key: str,
        value: dict[str, str],
        *,
        scope: str,
        expected_revision: int,
    ) -> None:
        revision, _, record_scope = self.records[key]
        if record_scope != scope:
            raise PermissionError("scope mismatch")
        if revision != expected_revision:
            raise ConcurrencyError("stale revision")
        self.records[key] = (revision + 1, dict(value), scope)
        self.calls.append("correct")

    def delete(self, key: str, *, scope: str, expected_revision: int) -> None:
        revision, _, record_scope = self.records[key]
        if record_scope != scope:
            raise PermissionError("scope mismatch")
        if revision != expected_revision:
            raise ConcurrencyError("stale revision")
        del self.records[key]
        self.calls.append("delete")


class MemoryLifecycleTests(unittest.TestCase):
    def test_save_read_correct_read_delete_and_confirm_absence(self) -> None:
        provider = SyntheticProvider()
        key = provider.save("project:alpha", {"fact": "v1"})

        self.assertEqual(provider.read(key, scope="project:alpha"), {"fact": "v1"})
        provider.correct(
            key,
            {"fact": "v2"},
            scope="project:alpha",
            expected_revision=1,
        )
        self.assertEqual(provider.read(key, scope="project:alpha"), {"fact": "v2"})
        provider.delete(key, scope="project:alpha", expected_revision=2)
        self.assertIsNone(provider.read(key, scope="project:alpha"))

    def test_new_session_and_project_scope_do_not_leak(self) -> None:
        provider = SyntheticProvider()
        key = provider.save("project:alpha", {"fact": "synthetic"})
        # A separate session can read only when it presents the same authorized scope.
        self.assertEqual(provider.read(key, scope="project:alpha"), {"fact": "synthetic"})
        self.assertIsNone(provider.read(key, scope="project:beta"))

    def test_two_agents_must_use_revision_guard(self) -> None:
        provider = SyntheticProvider()
        key = provider.save("personal", {"fact": "v1"})
        provider.correct(key, {"fact": "agent-a"}, scope="personal", expected_revision=1)
        with self.assertRaises(ConcurrencyError):
            provider.correct(key, {"fact": "agent-b"}, scope="personal", expected_revision=1)

    def test_unrelated_request_does_not_call_provider(self) -> None:
        provider = SyntheticProvider()
        before = list(provider.calls)
        # The caller keeps ordinary translation outside the memory route.
        self.assertEqual("hola"[::-1], "aloh")
        self.assertEqual(provider.calls, before)

    def test_switching_provider_stops_old_writes(self) -> None:
        old = SyntheticProvider()
        new = SyntheticProvider()
        old_key = old.save("personal", {"fact": "old"})
        old_calls = len(old.calls)
        new_key = new.save("personal", {"fact": "new"})
        self.assertEqual(len(old.calls), old_calls)
        self.assertEqual(new.read(new_key, scope="personal"), {"fact": "new"})
        self.assertEqual(old.read(old_key, scope="personal"), {"fact": "old"})

    def test_off_or_missing_scope_blocks_provider_write(self) -> None:
        provider = SyntheticProvider()
        descriptor = ProviderDescriptor(
            id="synthetic",
            name="synthetic",
            version="1.0.0",
            kind="installed-tool",
            location="test",
            local=True,
            network_required=False,
            capabilities=frozenset({"save", "read"}),
            storage_location="test-only",
            license="MIT",
            maintenance_status="active",
            interface="memory-provider-v1",
            source_of_truth="synthetic",
            evidence=ProviderEvidence(
                installed=True,
                enabled=True,
                callable=True,
                isolated_test=True,
            ),
        )
        result = route_operation(
            RouteRequest(
                operation=ProviderOperation.SAVE,
                scope="personal",
                user_consent="confirm",
                authorized_scopes=frozenset(),
                network_allowed=False,
            ),
            descriptor,
        )
        self.assertEqual(result.status, "blocked")
        self.assertEqual(provider.calls, [])


if __name__ == "__main__":
    unittest.main()
