import unittest
from Services.Builders.StaffBuilder import StaffBuilder

class TestMusicScoreBuilder(unittest.TestCase):

    # Test method init_score initializes score properties correctly
    def test_init_score(self):
        #top_staff, score_title, score_credits
        # Arrange
        score = None