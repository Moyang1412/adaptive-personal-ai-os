#!/usr/bin/env python3
"""Executable checks for the provider assessment and routing contract."""

from __future__ import annotations

import unittest
from dataclasses import replace

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
    base_capabilities = {
        "save",
        "read",
        "correct",
        "delete",
        "scope",
        "cross_session",
        "import_export",
        *({"cross_agent", "concurrent_write_guard"} if cross_agent else set()),
    }
    if capabilities is not None:
        base_capabilities = capabilities
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
    def test_false_valued_maps_are_not_capability_or_scope_lists(self) -> None:
        requirements = MemoryRequirements(True, {'read'}, False, True, 'confirm')
        with self.assertRaises(ValueError):
            recommend_plan(requirements, native_available=True,
                           native_capabilities={'read': False, 'cross_session': False}, providers=[])
        for field in ('capabilities', 'verified_capabilities', 'unverified_capabilities'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                replace(descriptor('map-rejected'), **{field: {'read': False}})
        for field in ('required_capabilities', 'private_profile_verified_capabilities'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                replace(requirements, **{field: {'read': False}})
        with self.assertRaises(ValueError):
            RouteRequest(ProviderOperation.READ, 'personal', 'authorized', {'personal': False}, False, persistent_required=True)

    def test_malformed_collection_members_fail_with_value_error(self) -> None:
        for invalid in (None, 12, 'read', [None], ['read', 3], [{}]):
            with self.subTest(value=invalid):
                with self.assertRaises(ValueError):
                    replace(descriptor('bad-collection'), capabilities=invalid)
                with self.assertRaises(ValueError):
                    MemoryRequirements(True, invalid, False, True, 'confirm')
                with self.assertRaises(ValueError):
                    RouteRequest(ProviderOperation.READ, 'p', 'authorized', invalid, False, persistent_required=True)

    def test_nontext_descriptor_and_route_fields_fail_early(self) -> None:
        for field in ('id', 'name', 'version', 'kind', 'location', 'storage_location',
                      'license', 'maintenance_status', 'interface', 'source_of_truth'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                replace(descriptor('bad-text'), **{field: 123})
        for field in ('scope', 'user_consent', 'active_provider_id'):
            request = RouteRequest(ProviderOperation.READ, 'p', 'authorized', {'p'}, False, persistent_required=True)
            with self.subTest(field=field), self.assertRaises(ValueError):
                replace(request, **{field: 123})
        with self.assertRaises(ValueError):
            MemoryRequirements(True, {'read'}, False, True, [])

    def test_supported_collections_retain_verified_native_positive(self) -> None:
        for collection in (list, tuple, set, frozenset):
            requirements = MemoryRequirements(True, collection(['read']), False, True, 'confirm')
            plan = recommend_plan(requirements, native_available=True,
                                  native_capabilities=collection(['read', 'cross_session', 'scope']), providers=[])
            self.assertEqual(plan.option, 'A')

    def test_caller_mutation_does_not_expand_verified_capabilities_or_scopes(self) -> None:
        capabilities = {'read', 'scope', 'cross_session'}
        verified = {'read', 'scope', 'cross_session'}
        base = descriptor('snapshot')
        candidate = ProviderDescriptor(**{**base.__dict__, 'capabilities': capabilities,
            'verified_capabilities': verified, 'unverified_capabilities': frozenset()})
        scopes = {'project-one'}
        request = RouteRequest(ProviderOperation.READ, 'project-two', 'authorized', scopes,
                               False, persistent_required=True, active_provider_id='snapshot')
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
                              native_capabilities={'save', 'read', 'cross_session', 'scope'}, providers=providers())
        self.assertEqual(plan.option, 'A')

    def test_text_boolean_cannot_claim_verified_evidence(self) -> None:
        with self.assertRaises(ValueError):
            ProviderEvidence(documented="false", installed="false", enabled="false",
                             callable="false", isolated_test="false")

    def test_text_boolean_cannot_authorize_network_or_sharing(self) -> None:
        for field in ['network_allowed', 'persistent_required', 'relevant', 'cross_agent', 'sharing_authorized', 'single_writer']:
            with self.subTest(field=field), self.assertRaises(ValueError):
                values = dict(operation=ProviderOperation.READ, scope='project', user_consent='authorized',
                              authorized_scopes={'project'}, network_allowed=False, persistent_required=True)
                values[field] = 'false'
                RouteRequest(**values)

    def test_text_boolean_cannot_change_persistence_requirements(self) -> None:
        with self.assertRaises(ValueError):
            MemoryRequirements('false', frozenset({'read'}), False, False, 'confirm')
        base = descriptor('strict')
        with self.assertRaises(ValueError):
            ProviderDescriptor(**{**base.__dict__, 'network_required': 'false'})

    def test_scope_text_is_not_split_into_individual_authorizations(self) -> None:
        with self.assertRaises(ValueError):
            RouteRequest(ProviderOperation.READ, 'p', 'authorized', 'project', False, persistent_required=True)

    def test_native_availability_must_be_a_boolean(self) -> None:
        requirements = MemoryRequirements(True, frozenset({'read'}), False, False, 'confirm')
        with self.assertRaises(ValueError):
            recommend_plan(requirements, native_available='false', native_capabilities={'read'}, providers=[])

    def test_trigger_runs_only_on_first_long_term_need(self) -> None:
        self.assertTrue(evaluate_trigger(first_long_term_need=True, already_evaluated=False))
        self.assertFalse(evaluate_trigger(first_long_term_need=True, already_evaluated=True))
        self.assertFalse(evaluate_trigger(first_long_term_need=False, already_evaluated=False))

    def test_changed_context_rechecks_only_a_relevant_continuity_need(self) -> None:
        self.assertTrue(evaluate_trigger(first_long_term_need=True, already_evaluated=True, context_changed=True))
        self.assertFalse(evaluate_trigger(first_long_term_need=False, already_evaluated=True, context_changed=True))
        self.assertFalse(evaluate_trigger(first_long_term_need=True, already_evaluated=True, context_changed=False))
        with self.assertRaises(ValueError):
            evaluate_trigger(first_long_term_need=True, already_evaluated=True, context_changed='false')

    def test_native_memory_wins_when_no_gap_is_present(self) -> None:
        requirements = MemoryRequirements(
            persistent=True,
            required_capabilities={"save", "read", "delete"},
            cross_agent=False,
            explicit_gap=False,
            user_consent="confirm",
        )
        plan = recommend_plan(requirements, native_available=True, native_capabilities=requirements.required_capabilities | {'cross_session', 'scope'}, providers=[])
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
            private_profile_verified_capabilities={"save", "read", "scope", "cross_agent", "cross_session", "concurrent_write_guard"},
        )
        plan = recommend_plan(requirements, native_available=True, native_capabilities={"save", "read"}, providers=[])
        self.assertEqual(plan.option, "B")
        self.assertTrue(plan.requires_explicit_scope)

    def test_profile_permission_does_not_supply_missing_capability_evidence(self) -> None:
        for capabilities in (set(), {'read', 'cross_agent'}, {'read', 'scope', 'cross_agent', 'cross_session', 'concurrent_write_guard'}):
            requirements = MemoryRequirements(
                True, {'read', 'delete', 'cross_agent'}, True, True, 'confirm',
                private_profile_authorized=True, private_profile_conflict_control=True,
                private_profile_verified_capabilities=capabilities,
            )
            plan = recommend_plan(requirements, native_available=True, native_capabilities={'read'}, providers=[])
            self.assertEqual(plan.option, 'D')
            self.assertTrue(any('授权不等于' in reason for reason in plan.reasons))

    def test_persistent_need_requires_cross_session_evidence(self) -> None:
        requirements = MemoryRequirements(True, {'read'}, False, True, 'confirm')
        plan = recommend_plan(requirements, native_available=True, native_capabilities={'read'}, providers=[])
        self.assertEqual(plan.option, 'D')
        empty = descriptor('no-capabilities', capabilities=set())
        self.assertEqual(empty.capabilities, frozenset())
        self.assertFalse(assess_provider(empty, requirements).eligible)
        candidate = descriptor('session-only-reader', capabilities={'read', 'scope'})
        assessment = assess_provider(candidate, requirements)
        self.assertFalse(assessment.eligible)
        self.assertIn('cross_session', assessment.unsupported_capabilities)
        self.assertEqual(recommend_plan(requirements, native_available=False, native_capabilities=set(), providers=[candidate]).option, 'D')
        self.assertEqual(recommend_plan(requirements, native_available=True, native_capabilities={'read', 'cross_session', 'scope'}, providers=[]).option, 'A')

    def test_profile_requires_scoping_and_guard_in_addition_to_requested_operations(self) -> None:
        for missing in ('scope', 'concurrent_write_guard'):
            capabilities = {'read', 'cross_agent', 'cross_session', 'scope', 'concurrent_write_guard'} - {missing}
            requirements = MemoryRequirements(
                True, {'read', 'cross_agent'}, True, True, 'confirm',
                private_profile_authorized=True, private_profile_conflict_control=True,
                private_profile_verified_capabilities=capabilities,
            )
            self.assertEqual(recommend_plan(requirements, native_available=True, native_capabilities={'read'}, providers=[]).option, 'D')

    def test_profile_capabilities_are_immutable_and_validated(self) -> None:
        supplied = {'read', 'scope', 'cross_agent', 'cross_session', 'concurrent_write_guard'}
        requirements = MemoryRequirements(True, {'read', 'cross_agent'}, True, True, 'confirm',
                                          private_profile_verified_capabilities=supplied)
        supplied.add('delete')
        self.assertNotIn('delete', requirements.private_profile_verified_capabilities)
        for invalid in ('read', {'invented'}, {123}):
            with self.assertRaises(ValueError):
                MemoryRequirements(True, {'read'}, False, False, 'confirm', private_profile_verified_capabilities=invalid)

    def test_verified_profile_still_needs_authorization_and_active_guard(self) -> None:
        for authorized, controlled in ((False, True), (True, False)):
            requirements = MemoryRequirements(
                True, {'read', 'cross_agent'}, True, True, 'confirm',
                private_profile_authorized=authorized, private_profile_conflict_control=controlled,
                private_profile_verified_capabilities={'read', 'scope', 'cross_agent', 'cross_session', 'concurrent_write_guard'},
            )
            self.assertEqual(recommend_plan(requirements, native_available=True, native_capabilities={'read'}, providers=[]).option, 'D')

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

    def test_equally_eligible_providers_are_not_ranked_by_their_names(self) -> None:
        requirements = MemoryRequirements(True, frozenset({'save', 'read'}), False, True, 'confirm')
        first = descriptor('aaa-provider', source_of_truth='source-one')
        second = descriptor('zzz-provider', source_of_truth='source-two')
        for providers in ([first, second], [second, first]):
            plan = recommend_plan(requirements, native_available=False, native_capabilities=set(), providers=providers)
            self.assertIsNone(plan.provider_id)
            self.assertEqual(plan.option, 'D')
            self.assertEqual(plan.candidate_provider_ids, ('aaa-provider', 'zzz-provider'))
            self.assertTrue(plan.requires_explicit_scope)

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
            persistent_required=True,
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
            persistent_required=True,
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
            persistent_required=True,
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
            persistent_required=True,
            active_provider_id="old",
        )
        result = route_operation(request, candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("明确授权", result.reason)

    def test_route_requires_verified_scope_and_relevance(self) -> None:
        candidate = descriptor("selected", capabilities={"save", "read", "cross_session"})
        request = RouteRequest(
            operation=ProviderOperation.READ,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            persistent_required=True,
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
            persistent_required=True,
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
            persistent_required=True,
            active_provider_id="shared",
            cross_agent=True,
            sharing_authorized=True,
        )
        self.assertEqual(route_operation(request, candidate).status, "provider")

        unguarded = descriptor(
            "unguarded",
            capabilities={"save", "read", "scope", "cross_agent", "cross_session"},
        )
        unguarded_request = RouteRequest(
            operation=ProviderOperation.SAVE,
            scope="personal",
            user_consent="authorized",
            authorized_scopes={"personal"},
            network_allowed=False,
            persistent_required=True,
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
            persistent_required=True,
            active_provider_id="verified-engine",
        )
        self.assertEqual(route_operation(request, candidate).status, "blocked")


if __name__ == "__main__":
    unittest.main()
