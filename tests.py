import unittest
from event import Event

class TestGameLogic(unittest.TestCase):

    def test_meets_criteria_true(self):
        player_stats = {"bilingual": 8, "athletic": 6, "academic": 9, "military": 7, "social": 5}
        criteria = {"bilingual": 5, "athletic": 5, "academic": 7, "military": 6, "social": 4}
        self.assertTrue(Event.meet_criteria(player_stats, criteria))

    def test_meets_criteria_false(self):
        player_stats = {"bilingual": 4, "athletic": 6, "academic": 9, "military": 7, "social": 5}
        criteria = {"bilingual": 5, "athletic": 5, "academic": 7, "military": 6, "social": 4}
        self.assertFalse(Event.meet_criteria(player_stats, criteria))

    def test_meets_criteria_edge_case_equal(self):
        player_stats = {"bilingual": 5, "athletic": 5, "academic": 7, "military": 6, "social": 4}
        criteria = {"bilingual": 5, "athletic": 5, "academic": 7, "military": 6, "social": 4}
        self.assertTrue(Event.meet_criteria(player_stats, criteria))  # Should be True because we check "greater than"

    def test_meets_criteria_missing_keys(self):
        player_stats = {"bilingual": 8, "athletic": 6}  # Missing some stats
        criteria = {"bilingual": 5, "athletic": 5, "academic": 7, "military": 6, "social": 4}
        self.assertFalse(Event.meet_criteria(player_stats, criteria))  # Missing keys default to 0

if __name__ == "__main__":
    unittest.main()