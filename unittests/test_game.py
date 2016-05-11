from mock.mock import PropertyMock

from core.game import KniffelGame
from unittest import TestCase
from mock import patch


class TestKniffelGame(TestCase):

    def test_players(self):

        game = KniffelGame()
        self.assertEqual(0, len(game.players))

        game.add_player("dummy")
        self.assertEqual(1, len(game.players))

    def test_players_order(self):

        order = None

        for game in (KniffelGame() for _ in range(100)):
            for number in range(5):
                game.add_player(number)
                game._shuffle()
                if order is not None and order != game.players:
                    return

                order = game.players

        raise AssertionError

    def test_new_round(self):

        game = KniffelGame()

        game._current_rolled_die = [6] * 2
        game._current_saved_die = [6] * 2
        game._set_new_round("dummy_player")
        self.assertIsNone(game._current_rolled_die)
        self.assertIsNone(game._current_saved_die)

    def test_roll_count(self):

        game = KniffelGame()

        self.assertRaises(AttributeError, getattr, game, '_roll_times')

        game._set_new_round("dummy_player")
        self.assertEqual(game._roll_times, 0)
        game.roll()
        self.assertEqual(game._roll_times, 1)

        game.roll()
        game.roll()
        self.assertEqual(game._roll_times, 3)

        self.assertRaises(Exception, game.roll)

    def test_round(self):

        game = KniffelGame()
        game._current_saved_die = [6] * 2

        # Die shall be reset
        game._set_new_round("dummy_player")
        self.assertFalse(game._current_saved_die)

    def test_die_state(self):

        game = KniffelGame()

        game._set_new_round("dummy_player")
        self.assertEqual(5, len(game.roll()))

        game._set_new_round("dummy_player")
        game._current_saved_die = [1] * 4
        rolled_die = game.roll()
        self.assertEqual(1, len(rolled_die))
        self.assertEqual(rolled_die, game._current_rolled_die)

        # Test implausible scenarios
        game._set_new_round("dummy_player")
        game._current_saved_die = [1] * 5
        self.assertRaises(AssertionError, game.roll)

        game._set_new_round("dummy_player")
        game._current_saved_die = [1] * 6
        self.assertRaises(AssertionError, game.roll)

    def test_save(self):

        game = KniffelGame()

        game._set_new_round("dummy_player")
        # Assertion error upon saving die before rolling
        self.assertRaises(AssertionError, game.save, [6, 6, 6, 6, 6])

        # Assertion error upon saving die which were not rolled
        game._current_saved_die = [1] * 4
        game._current_rolled_die = [2]
        self.assertRaises(AssertionError, game.save, [6])

    def test_check_die_availability(self):

        game = KniffelGame()

        game._set_new_round("dummy_player")

        self.assertRaises(TypeError, game._check_die_availability, [1])

        game._current_rolled_die = [1] * 3
        self.assertFalse(game._check_die_availability([6]))
        self.assertFalse(game._check_die_availability([1] * 5))
        self.assertTrue(game._check_die_availability([1]))
        self.assertTrue(game._check_die_availability([1] * 2))

        game._set_new_round("dummy_player")
        game._current_rolled_die = [1]
        game._current_saved_die = [5] * 2
        self.assertFalse(game._check_die_availability([6]))
        self.assertFalse(game._check_die_availability([5] * 3))
        self.assertTrue(game._check_die_availability([5]))
        self.assertTrue(game._check_die_availability([5] * 2))

    def test_calculate_score(self):

        game = KniffelGame()

        player = "dummy_player"

        game.add_player(player)

        game._set_new_round(player)
        game.roll()
        game._current_rolled_die = [2] * 5

        self.assertRaises(Exception, game.calculate_score, "SOME INVALID SCORE")

        dummy_die = [5] * 3 + [2] + [1]
        kniffel_of_fours = [4] * 5
        four = [1] * 4 + [5]
        poor = [1, 2, 3, 4, 5]

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.ONES), 1)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.TWOS), 2)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.THREES), 0)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.FOURS), 0)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.FIVES), 5*3)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.SIXES), 0)

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.SIXES), 6*5)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.THREE_X), sum(dummy_die))

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.THREE_X), 6*5)

        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.THREE_X), 0)

        with patch.object(game, '_current_rolled_die', four):
            self.assertEqual(game.calculate_score(game.FOUR_X), sum(four))

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.FOUR_X), 6*5)

        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.FOUR_X), 0)

    def test_score(self):

        game = KniffelGame()

        player = "dummy_player"

        game.add_player(player)

        game._set_new_round(player)
        game.roll()
        game._current_rolled_die = [2] * 5

        self.assertRaises(AssertionError, game.score, "SOME INVALID SCORE")

