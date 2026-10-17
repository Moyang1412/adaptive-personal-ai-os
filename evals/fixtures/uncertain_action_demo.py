"""Executable illustration, NOT a ZhiXu agent evaluation or production retry layer.

All effects are fictional in-memory rows. No network, accounts or file writes.
The deliberately naive caller is NOT an observed previous ZhiXu/model response.
"""
import json


class SyntheticService:
    def __init__(self):
        self.rows = []
        self.receipts = {}

    def create(self, title, *, key=None, lose_response=False):
        if key is not None and key in self.receipts:
            old = self.receipts[key]
            if old['title'] != title:
                raise ValueError('same key with different intent')
            return dict(old)
        row = {'id': len(self.rows) + 1, 'title': title}
        self.rows.append(row)
        if key is not None:
            self.receipts[key] = row
        if lose_response:
            raise TimeoutError('response lost AFTER the fictional effect')
        return dict(row)

    def receipt(self, key):
        # This fixture is strongly consistent and same-process; real providers
        # may have delayed reads, missing request identifiers or expiry windows.
        result = self.receipts.get(key)
        return dict(result) if result else None


def demonstrate():
    naive = SyntheticService()
    try:
        naive.create('fictional library reminder', lose_response=True)
    except TimeoutError:
        naive.create('fictional library reminder')

    checked = SyntheticService()
    try:
        checked.create('fictional library reminder', key='intent-1', lose_response=True)
    except TimeoutError:
        observed = checked.receipt('intent-1')
    if observed is None:
        raise AssertionError('fixture receipt missing')
    replay = checked.create('fictional library reminder', key='intent-1')
    if replay != observed or len(naive.rows) != 2 or len(checked.rows) != 1:
        raise AssertionError('unexpected synthetic state')

    replay_effects = len(checked.rows)
    try:
        checked.create('different fictional task', key='intent-1')
    except ValueError:
        changed_intent_rejected = True
    else:
        changed_intent_rejected = False

    # Forgetting an idempotency receipt illustrates an expired deduplication
    # horizon. Reusing the same key alone no longer provides at-most-once behavior.
    checked.receipts.clear()
    checked.create('fictional library reminder', key='intent-1')
    return {'naive_repeat_effects': len(naive.rows),
            'reconciled_then_supported_replay_effects': replay_effects,
            'changed_intent_rejected': changed_intent_rejected,
            'effects_after_receipt_expiry_and_replay': len(checked.rows),
            'scope': 'Scripted synthetic service/callers only. No actual agent, provider, persistence, concurrency or end-user behavior was evaluated.'}


if __name__ == '__main__':
    print(json.dumps(demonstrate(), indent=2))
