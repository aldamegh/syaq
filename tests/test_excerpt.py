import json
import unittest
from pathlib import Path
from datetime import datetime, timezone
from app.normalize import normalize_for_game
from app.public_games import is_game_released, public_games_payload, riyadh_today
from app.log_safety import safe_url_for_log

ROOT = Path(__file__).resolve().parents[1]

class ExcerptTests(unittest.TestCase):
    def test_synthetic_normalization_contract(self):
        corpus = json.loads((ROOT / 'normalization/conformance-corpus-v1.json').read_text(encoding='utf-8'))
        self.assertTrue(corpus['fixtures_are_synthetic'])
        for case in corpus['cases']:
            with self.subTest(case=case['id']):
                self.assertEqual(normalize_for_game(case['input']), case['expected'])

    def test_yeh_and_maqsura_remain_distinct(self):
        self.assertNotEqual(normalize_for_game('سي'), normalize_for_game('سى'))

    def test_non_string_is_rejected(self):
        with self.assertRaises(TypeError):
            normalize_for_game(None)

    def test_public_payload_excludes_answers(self):
        game = {'game_id': 1, 'target_words': ['synthetic'], 'private_note': 'synthetic'}
        self.assertEqual(public_games_payload([game], 1), {'games': [{'id': 1}], 'active_id': 1})

    def test_release_uses_riyadh_midnight(self):
        at = datetime(2026, 1, 1, 21, tzinfo=timezone.utc)
        self.assertEqual(riyadh_today(at).isoformat(), '2026-01-02')
        self.assertTrue(is_game_released({'scheduled_date': '2026-01-02'}, at=at))
        self.assertFalse(is_game_released({'scheduled_date': '2026-01-03'}, at=at))
        self.assertFalse(is_game_released({'scheduled_date': 'invalid'}, at=at))

    def test_log_url_removes_userinfo_query_and_fragment(self):
        value = 'https://example-user:example-password@example.invalid/path?token=example#fragment'
        self.assertEqual(safe_url_for_log(value), 'https://example.invalid/path')
        self.assertEqual(safe_url_for_log('invalid'), '<configured>')

if __name__ == '__main__':
    unittest.main()
