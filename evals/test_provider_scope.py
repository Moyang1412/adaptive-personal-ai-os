"""Selection and operation routing must agree about required scope evidence."""
import unittest
from dataclasses import replace

try:
    from .provider_selection import (
        MemoryRequirements, ProviderOperation, RouteRequest,
        assess_provider, recommend_plan, route_operation,
    )
    from .test_provider_selection import descriptor
except ImportError:
    from provider_selection import (
        MemoryRequirements, ProviderOperation, RouteRequest,
        assess_provider, recommend_plan, route_operation,
    )
    from test_provider_selection import descriptor


class ProviderScopeTests(unittest.TestCase):
    def setUp(self):
        self.requirements = MemoryRequirements(True, {'read'}, False, True, 'confirm')

    def test_persistence_alone_does_not_make_unscoped_native_memory_eligible(self):
        plan = recommend_plan(self.requirements, native_available=True,
                              native_capabilities={'read', 'cross_session'}, providers=[])
        self.assertEqual(plan.option, 'D')

    def test_missing_or_unverified_scope_blocks_external_selection(self):
        missing = descriptor('missing-scope', capabilities={'read', 'cross_session'})
        unverified = replace(descriptor('unverified-scope'),
                             verified_capabilities=frozenset({'read', 'cross_session'}),
                             unverified_capabilities=frozenset({'scope'}))
        for provider in (missing, unverified):
            with self.subTest(provider=provider.id):
                assessment = assess_provider(provider, self.requirements)
                self.assertFalse(assessment.eligible)
                self.assertIn('scope', assessment.unsupported_capabilities | assessment.unverified_capabilities)
                plan = recommend_plan(self.requirements, native_available=False,
                                      native_capabilities=set(), providers=[provider])
                self.assertEqual(plan.option, 'D')

    def test_verified_scoped_native_memory_stays_native_first(self):
        def unavailable_registry():
            raise AssertionError('no external probe needed')
            yield
        plan = recommend_plan(self.requirements, native_available=True,
                              native_capabilities={'read', 'scope', 'cross_session'},
                              providers=unavailable_registry())
        self.assertEqual(plan.option, 'A')

    def test_recommended_read_provider_has_routable_scope(self):
        provider = descriptor('scoped-reader', capabilities={'read', 'scope', 'cross_session'})
        plan = recommend_plan(self.requirements, native_available=False,
                              native_capabilities=set(), providers=[provider])
        self.assertEqual(plan.option, 'C')
        request = RouteRequest(ProviderOperation.READ, 'project:demo', 'authorized',
                               {'project:demo'}, False, active_provider_id=plan.provider_id)
        self.assertEqual(route_operation(request, provider).status, 'provider')
        self.assertEqual(route_operation(replace(request, scope='project:other'), provider).status, 'blocked')


if __name__ == '__main__':
    unittest.main()
