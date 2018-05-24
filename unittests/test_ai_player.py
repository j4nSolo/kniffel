
from core.game import KniffelGame
from unittest import TestCase
from sample.stupid_ai_player import StupidAIPlayer
from mock import patch


class TestAIPlayer(TestCase):

    @patch.object(KniffelGame, 'roll')
    @patch.object(KniffelGame, 'score')
    def test_round(self, roll_mock, score_mock):

        game = KniffelGame()
        player = StupidAIPlayer("dummy name")
        game.add_player(player)

        self.assertFalse(roll_mock.called)

        player.round(game)

        # Assert that the 'roll' method from game has been called once at least
        self.assertTrue(roll_mock.called)

        # Assert that the player has called the 'roll' method at most 3 times
        self.assertLessEqual(roll_mock.call_count, 3)

        self.assertTrue(score_mock.called)

