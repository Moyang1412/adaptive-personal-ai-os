#!/usr/bin/env python3
"""Executable checks for the provider assessment and routing contract."""

from __future__ import annotations

import unittest

try:
    from .provider_selection import (
        MemoryRequirements,
        ProviderDescriptor,
        ProviderEvidence,
        ProviderOperation,
        RouteRequest,
        SourceConflictError,
        assess_provider,
        evaluate_trigger,
        recommend_plan,
        route_operation,
    )
except ImportError:  # Direct ``python evals/test_provider_selection.py``.
    from provider_selection import (
        MemoryRequirements,
        ProviderDescriptor,
        ProviderEvidence,
        ProviderOperation,
        RouteRequest,
        SourceConflictError,
        assess_provider,
        evaluate_trigger,
        recommend_plan,
        route_operation,
    )


def descriptor(
    provider_id: str,
    *,
    kind: str = "installed-tool",
    capabilities: set[str] | None = None,
    evidence: ProviderEvidence | None = None,
    source_of_truth: str = "synthetic-profile",
    cross_agent: bool = False,
    local: bool = True,
    network_required: bool = False,
    license_name: str = "Apache-2.0",
    maintenance: str = "active",
) -> ProviderDescriptor:
    base_capabilities = capabilities or {
        "save",
        "read",
        "correct",
        "delete",
        "scope",
        "cross_session",
        "import_export",
        *({"cross_agent", "concurrent_write_guard"} if cross_agent else set()),
    }
    actual_evidence = evidence or ProviderEvidence(
        documented=True,
        installed=True,
        enabled=True,
        callable=True,
        isolated_test=True,
    )
    return ProviderDescriptor(
        id=provider_id,
        name=provider_id,
        version="1.0.0",
        kind=kind,
        location="isolated-test",
        local=local,
        network_required=network_required,
        capabilities=base_capabilities,
        storage_location="synthetic-only",
        license=license_name,
        maintenance_status=maintenance,
        interface="memory-provider-v1",
        source_of_truth=source_of_truth,
        evidence=actual_evidence,
        verified_capabilities=frozenset(
            base_capabilities if actual_evidence.isolated_test else set()
        ),
    )


class ProviderSelectionTests(unittest.TestCase):
    def test_caller_mutation_does_not_expand_verified_capabilities_or_scopes(self) -> None:
        capabilities = {'read', 'scope'}
        verified = {'read', 'scope'}
        base = descriptor('snapshot')
        candidate = ProviderDescriptor(**{**base.__dict__, 'capabilities': capabilities,
            'verified_capabilities': verified, 'unverified_capabilities': frozenset()})
        scopes = {'project-one'}
        request = RouteRequest(ProviderOperation.READ, 'project-two', 'authorized', scopes,
                               False, active_provider_id='snapshot')
        capabilities.add('save'); verified.add('save'); scopes.add('project-two')
        self.assertNotIn('save', candidate.verified_capabilities)
        self.assertNotIn('project-two', request.authorized_scopes)
        self.assertEqual(route_operation(request, candidate).status, 'blocked')

    def test_duplicate_provider_identity_is_rejected(self) -> None:
        requirements = MemoryRequirements(True, frozenset({'save', 'read'}), False, True, 'confirm')
        with self.assertRaises(SourceConflictError):
            recommend_plan(requirements, native_available=False, native_capabilities=set(), providers=[
                descriptor('duplicate', source_of_truth='scope-one'),
                descriptor('duplicate', source_of_truth='scope-two'),
            ])

    def test_disabled_or_session_only_memory_does_not_enumerate_providers(self) -> None:
        def providers():
            raise AssertionError('unneeded provider enumeration')
            yield
        for persistent, consent in [(True, 'off'), (False, 'confirm')]:
            requirements = MemoryRequirements(persistent, frozenset({'read'}), False, False, consent)
            plan = recommend_plan(requirements, native_available=False,
                                  native_capabilities=set(), providers=providers())
            self.assertEqual(plan.option, 'D')

    def test_sufficient_native_memory_does_not_probe_unneeded_providers(self) -> None:
        def providers():
            raise AssertionError('native-first selection must not probe external registry')
            yield
        requirements = MemoryRequirements(True, frozenset({'save', 'read'}), False, False, 'confirm')
        plan = recommend_plan(requirements, native_available=True,
                              native_capabilities={'save', 'read'}, providers=providers())
        self.assertEqual(plan.option, 'A')

    def test_trigger_runs_only_on_first_long_term_need(self) -> None:
        self.assertTrue(evaluate_trigger(first_long_term_need=True, already_evaluated=False))
        self.assertFalse(evaluate_trigger(first_long_term_need=True, already_evaluated=True))
        self.assertFalse(evaluate_trigger(first_long_term_need=False, already_evaluated=False))

    def test_native_memory_wins_when_no_gap_is_present(self) -> None:
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read", "delete"},
            cross_agent=False,
            explicit_gap=False,
            user_consent="confirm",
        )
        plan = recommend_plan(requirements, native_available=True, native_capabilities=requirements.required_capabilities, providers=[])
        self.assertEqual(plan.option, "A")
        self.assertIsNone(plan.provider_id)

    def test_cross_agent_profile_is_recommended_only_with_explicit_scope(self) -> None:
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read", "scope", "cross_agent"},
            cross_agent=True,
            explicit_gap=True,
            user_consent="confirm",
            private_profile_authorized=True,
            private_profile_conflict_control=True,
        )
        plan = recommend_plan(requirements, native_available=True, native_capabilities={"save", "read"}, providers=[])
        self.assertEqual(plan.option, "B")
        self.assertTrue(plan.requires_explicit_scope)

    def test_installed_provider_is_not_recommended_from_installation_alone(self) -> None:
        candidate = descriptor(
            "installed-but-unverified",
            evidence=ProviderEvidence(
                documented=True,
                installed=True,
                enabled=False,
                callable=False,
                isolated_test=False,
            ),
        )
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read"},
            cross_agent=False,
            explicit_gap=True,
            user_consent="confirm",
        )
        assessment = assess_provider(candidate, requirements)
        self.assertFalse(assessment.eligible)
        plan = recommend_plan(requirements, native_available=False, native_capabilities=set(), providers=[candidate])
        self.assertEqual(plan.option, "D")
        self.assertTrue(any("provider" in reason for reason in plan.reasons))

    def test_unknown_metadata_or_missing_documentation_is_not_eligible(self) -> None:
        for candidate in (
            descriptor("unknown-license", license_name="unknown"),
            descriptor(
                "undocumented",
                evidence=ProviderEvidence(
                    documented=False,
                    installed=True,
                    enabled=True,
                    callable=True,
                    isolated_test=True,
                ),
            ),
        ):
            requirements = MemoryRequirements(
                persistent=True,
                required_capabilities={"save", "read"},
                cross_agent=False,
                explicit_gap=True,
                user_consent="confirm",
            )
            self.assertFalse(assess_provider(candidate, requirements).eligible)

    def test_provider_with_verified_capabilities_can_fill_an_explicit_gap(self) -> None:
        candidate = descriptor("verified-engine", cross_agent=True)
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read", "delete", "cross_agent"},
            cross_agent=True,
            explicit_gap=True,
            user_consent="confirm",
        )
        plan = recommend_plan(requirements, native_available=True, native_capabilities={"save", "read"}, providers=[candidate])
        self.assertEqual(plan.option, "C")
        self.assertEqual(plan.provider_id, "verified-engine")

    def test_off_choice_never_routes_a_write(self) -> None:
        candidate = descriptor("verified-engine")
        request = RouteRequest(
            operation=ProviderOperation.SAVE,
            scope="project:synthetic",
            user_consent="off",
            authorized_scopes=set(),
            network_allowed=False,
            active_provider_id="verified-engine",
        )
        result = route_operation(request, candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("明确授权", result.reason)

    def test_no_permission_never_claims_success(self) -> None:
        candidate = descriptor("verified-engine", network_required=True, local=False)
        request = RouteRequest(
            operation=ProviderOperation.SAVE,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="verified-engine",
        )
        result = route_operation(request, candidate)
        self.assertEqual(result.status, "blocked")
        self.assertNotEqual(result.status, "saved")

    def test_export_uses_the_import_export_capability(self) -> None:
        candidate = descriptor("verified-engine")
        request = RouteRequest(
            operation=ProviderOperation.EXPORT,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="verified-engine",
        )
        result = route_operation(request, candidate)
        self.assertEqual(result.status, "provider")

    def test_file_fallback_is_not_promoted_to_a_mature_engine(self) -> None:
        candidate = descriptor("manual-file", kind="file-fallback")
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read"},
            cross_agent=False,
            explicit_gap=True,
            user_consent="confirm",
        )
        plan = recommend_plan(requirements, native_available=False, native_capabilities=set(), providers=[candidate])
        self.assertEqual(plan.option, "D")

    def test_switch_requires_explicit_migration_and_single_source(self) -> None:
        first = descriptor("first", source_of_truth="profile")
        second = descriptor("second", source_of_truth="profile")
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read"},
            cross_agent=False,
            explicit_gap=True,
            user_consent="confirm",
        )
        with self.assertRaises(SourceConflictError):
            recommend_plan(requirements, native_available=False, native_capabilities=set(), providers=[first, second])

    def test_unverified_capability_is_reported_separately(self) -> None:
        candidate = descriptor(
            "partial",
            capabilities={"save", "read"},
            evidence=ProviderEvidence(
                documented=True,
                installed=True,
                enabled=True,
                callable=True,
                isolated_test=False,
            ),
        )
        assessment = assess_provider(
            candidate,
            MemoryRequirements(
                persistent=True,
                required_capabilities={"save", "read"},
                cross_agent=False,
                explicit_gap=True,
                user_consent="confirm",
            ),
        )
        self.assertNotIn("save", assessment.verified_capabilities)
        self.assertIn("save", assessment.unverified_capabilities)

    def test_declared_unverified_capability_is_not_promoted(self) -> None:
        candidate = descriptor("partial-declared")
        candidate = ProviderDescriptor(
            **{
                **candidate.__dict__,
                "verified_capabilities": frozenset({"read", "scope"}),
                "unverified_capabilities": frozenset({"save"}),
            }
        )
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read"},
            cross_agent=False,
            explicit_gap=True,
            user_consent="confirm",
        )
        assessment = assess_provider(candidate, requirements)
        self.assertFalse(assessment.eligible)
        self.assertNotIn("save", assessment.verified_capabilities)
        self.assertIn("save", assessment.unverified_capabilities)

    def test_route_requires_explicit_authorization_and_current_provider(self) -> None:
        candidate = descriptor("selected")
        request = RouteRequest(
            operation=ProviderOperation.READ,
            scope="personal",
            user_consent="confirm",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="old",
        )
        result = route_operation(request, candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("明确授权", result.reason)

    def test_route_requires_verified_scope_and_relevance(self) -> None:
        candidate = descriptor("selected", capabilities={"save", "read"})
        request = RouteRequest(
            operation=ProviderOperation.READ,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="selected",
        )
        result = route_operation(request, candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("范围", result.reason)

        relevant_request = RouteRequest(
            operation=ProviderOperation.READ,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="selected",
            relevant=False,
        )
        self.assertEqual(route_operation(relevant_request, descriptor("selected")).status, "blocked")

    def test_cross_agent_route_requires_sharing_and_write_protection(self) -> None:
        candidate = descriptor("shared", cross_agent=True)
        request = RouteRequest(
            operation=ProviderOperation.SAVE,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="shared",
            cross_agent=True,
            sharing_authorized=True,
        )
        self.assertEqual(route_operation(request, candidate).status, "provider")

        unguarded = descriptor(
            "unguarded",
            capabilities={"save", "read", "scope", "cross_agent"},
        )
        unguarded_request = RouteRequest(
            operation=ProviderOperation.SAVE,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="unguarded",
            cross_agent=True,
            sharing_authorized=True,
        )
        self.assertEqual(route_operation(unguarded_request, unguarded).status, "blocked")

    def test_unknown_operation_is_blocked(self) -> None:
        candidate = descriptor("verified-engine")
        request = RouteRequest(
            operation="save",  # type: ignore[arg-type]
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            active_provider_id="verified-engine",
        )
        self.assertEqual(route_operation(request, candidate).status, "blocked")


if __name__ == "__main__":
    unittest.main()
