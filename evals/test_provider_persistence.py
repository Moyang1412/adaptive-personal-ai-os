"""Persistence requirements must survive selection-to-operation routing.

These are pure contract checks with fictional descriptors, not host persistence
tests. Explicit same-session inspection/cleanup still needs every other guard.
"""

import unittest
from dataclasses import replace

try:
    from .provider_selection import (
        MemoryRequirements, ProviderOperation, RouteRequest,
        recommend_plan, route_operation,
    )
    from .test_provider_selection import descriptor
except ImportError:
    from provider_selection import (
        MemoryRequirements, ProviderOperation, RouteRequest,
        recommend_plan, route_operation,
    )
    from test_provider_selection import descriptor


def request_for(operation, *, persistent_required):
    return RouteRequest(
        operation=operation,
        scope='project:demo',
        user_consent='authorized',
        authorized_scopes={'project:demo'},
        network_allowed=False,
        persistent_required=persistent_required,
        active_provider_id='selected',
    )


class ProviderPersistenceTests(unittest.TestCase):
    def test_persistent_read_and_save_cannot_bypass_rejected_selection(self):
        provider = descriptor('selected', capabilities={'read', 'save', 'scope'})
        for operation in (ProviderOperation.READ, ProviderOperation.SAVE):
            with self.subTest(operation=operation):
                requirements = MemoryRequirements(True, {operation.value}, False, True, 'authorized')
                plan = recommend_plan(requirements, native_available=False,
                                      native_capabilities=set(), providers=[provider])
                self.assertEqual(plan.option, 'D')
                result = route_operation(request_for(operation, persistent_required=requirements.persistent), provider)
                self.assertEqual(result.status, 'blocked')
                self.assertIn('跨会话', result.reason)

    def test_declared_but_unverified_persistence_blocks_all_required_routes(self):
        provider = descriptor('selected')
        provider = replace(provider,
                           verified_capabilities=provider.verified_capabilities - {'cross_session'},
                           unverified_capabilities={'cross_session'})
        for operation in ProviderOperation:
            with self.subTest(operation=operation):
                result = route_operation(request_for(operation, persistent_required=True), provider)
                self.assertEqual(result.status, 'blocked')
                self.assertIn('跨会话', result.reason)

    def test_qualified_provider_routes_each_explicit_persistence_request(self):
        provider = descriptor('selected')
        for operation in ProviderOperation:
            with self.subTest(operation=operation):
                result = route_operation(request_for(operation, persistent_required=True), provider)
                self.assertEqual(result.status, 'provider')
                self.assertEqual(result.provider_id, provider.id)
                self.assertNotIn(result.status, {'saved', 'deleted', 'completed'})

    def test_explicit_same_session_inspection_cleanup_and_export_remain_available(self):
        provider = descriptor('selected', capabilities={'read', 'delete', 'import_export', 'scope'})
        for operation in (ProviderOperation.READ, ProviderOperation.DELETE, ProviderOperation.EXPORT):
            with self.subTest(operation=operation):
                result = route_operation(request_for(operation, persistent_required=False), provider)
                self.assertEqual(result.status, 'provider')
                self.assertNotIn(result.status, {'saved', 'deleted', 'completed'})

    def test_nonpersistent_request_does_not_relax_authorization_or_capability(self):
        provider = descriptor('selected', capabilities={'read', 'delete', 'scope'})
        request = request_for(ProviderOperation.DELETE, persistent_required=False)
        for patch in ({'user_consent': 'off'}, {'user_consent': 'confirm'},
                      {'scope': 'project:other'}, {'active_provider_id': 'other'},
                      {'relevant': False}):
            with self.subTest(patch=patch):
                self.assertEqual(route_operation(replace(request, **patch), provider).status, 'blocked')
        for missing in ('scope', 'delete'):
            limited = replace(provider, verified_capabilities=provider.verified_capabilities - {missing})
            with self.subTest(missing=missing):
                self.assertEqual(route_operation(request, limited).status, 'blocked')

    def test_persistence_evidence_does_not_override_unavailable_or_unknown_operation(self):
        provider = descriptor('selected')
        for persistent_required in (True, False):
            for field in ('installed', 'enabled', 'callable', 'isolated_test'):
                unavailable = replace(provider, evidence=replace(provider.evidence, **{field: False}))
                with self.subTest(persistent_required=persistent_required, unavailable=field):
                    request = request_for(ProviderOperation.READ, persistent_required=persistent_required)
                    self.assertEqual(route_operation(request, unavailable).status, 'blocked')
            unknown = request_for('read', persistent_required=persistent_required)
            self.assertEqual(route_operation(unknown, provider).status, 'blocked')

    def test_persistence_requirement_is_explicit_and_boolean(self):
        with self.assertRaises(TypeError):
            RouteRequest(ProviderOperation.READ, 'project:demo', 'authorized', {'project:demo'}, False)
        for value in ('false', 0, 1, None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                request_for(ProviderOperation.READ, persistent_required=value)


if __name__ == '__main__':
    unittest.main()
