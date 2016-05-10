
from core.game import KniffelGame
from unittest import TestCase


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
        game._set_new_round()
        self.assertIsNone(game._current_rolled_die)
        self.assertIsNone(game._current_saved_die)



    def test_roll_count(self):

        game = KniffelGame()

        self.assertRaises(AttributeError, getattr, game, '_roll_times')

        game._set_new_round()
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
        game._set_new_round()
        self.assertFalse(game._current_saved_die)

    def test_die_state(self):

        game = KniffelGame()

        game._set_new_round()
        self.assertEqual(5, len(game.roll()))

        game._set_new_round()
        game._current_saved_die = [1] * 4
        self.assertEqual(1, len(game.roll()))

        # Test implausible scenarios
        game._set_new_round()
        game._current_saved_die = [1] * 5
        self.assertRaises(AssertionError, game.roll)

        game._set_new_round()
        game._current_saved_die = [1] * 6
        self.assertRaises(AssertionError, game.roll)

    def test_save(self):

        game = KniffelGame()

        game._set_new_round()
        # Assertion error upon saving die before rolling
        self.assertRaises(AssertionError, game.save, [6, 6, 6, 6, 6])

        # Assertion error upon saving die which were not rolled
        game._current_saved_die = [1] * 4
        game._current_rolled_die = [2]
        self.assertRaises(AssertionError, game.save, [6])
