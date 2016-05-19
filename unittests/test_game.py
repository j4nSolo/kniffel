from collections import OrderedDict
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

        self.assertIsNone(game._roll_times)

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

        # * Test implausible scenarios
        # Assertion error because of no available die to be rolled
        game._set_new_round("dummy_player")
        game._current_saved_die = [1] * 5
        self.assertRaises(AssertionError, game.roll)

        # Assertion error because of no available die to be rolled
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

        # Test no rolled die
        self.assertRaises(AssertionError, game._check_die_availability, [1])

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
        poorer = [1, 2, 3, 4, 6]
        full_house = [2] * 2 + [3] * 3
        all_upper_scores = {
            "dummy_player": OrderedDict(
                [(game.ONES, 1), (game.TWOS, 4), (game.THREES, 23), (game.FOURS, 2), (game.FIVES, 56), (game.SIXES, 0),
                 (game.KNIFFEL, 0)])
        }

        # Upper section
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
            self.assertEqual(game.calculate_score(game.SIXES), 0)

        with patch.object(game, '_current_rolled_die', dummy_die):
            self.assertEqual(game.calculate_score(game.THREE_X), sum(dummy_die))

        # Three of a kind
        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.THREE_X), 20)

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.THREE_X), sum(kniffel_of_fours))

        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.THREE_X), 0)

        # Four of a kind
        with patch.object(game, '_current_rolled_die', four):
            self.assertEqual(game.calculate_score(game.FOUR_X), sum(four))

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.FOUR_X), sum(kniffel_of_fours))

        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.FOUR_X), 0)

        # Full house
        with patch.object(game, '_current_rolled_die', full_house):
            self.assertEqual(game.calculate_score(game.FULL_HOUSE), 25)

        with patch.object(game, '_current_rolled_die', full_house[3:] + full_house[:3]):
            self.assertEqual(game.calculate_score(game.FULL_HOUSE), 25)

        with patch.object(game, '_current_rolled_die', kniffel_of_fours), \
             patch.object(game, '_scores', all_upper_scores):
            self.assertEqual(game.calculate_score(game.FULL_HOUSE), 25)

        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.FULL_HOUSE), 0)

        # Small straight
        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.SMALL_STRAIGHT), 30)

        with patch.object(game, '_current_rolled_die', poorer):
            self.assertEqual(game.calculate_score(game.SMALL_STRAIGHT), 30)

            with patch.object(game, '_current_rolled_die', kniffel_of_fours):
                self.assertEqual(game.calculate_score(game.SMALL_STRAIGHT), 0)

        with patch.object(game, '_current_rolled_die', kniffel_of_fours), \
             patch.object(game, '_scores', all_upper_scores):
            self.assertEqual(game.calculate_score(game.SMALL_STRAIGHT), 30)

        # Large straight
        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.LARGE_STRAIGHT), 40)

        with patch.object(game, '_current_rolled_die', poorer):
            self.assertEqual(game.calculate_score(game.LARGE_STRAIGHT), 00)

            with patch.object(game, '_current_rolled_die', kniffel_of_fours):
                self.assertEqual(game.calculate_score(game.LARGE_STRAIGHT), 0)

        with patch.object(game, '_current_rolled_die', kniffel_of_fours), \
             patch.object(game, '_scores', all_upper_scores):
            self.assertEqual(game.calculate_score(game.LARGE_STRAIGHT), 40)

        # Chance
        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.CHANCE), sum(poor))

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.CHANCE), sum(kniffel_of_fours))

        # Kniffel
        with patch.object(game, '_current_rolled_die', poor):
            self.assertEqual(game.calculate_score(game.KNIFFEL), 0)

        with patch.object(game, '_current_rolled_die', kniffel_of_fours):
            self.assertEqual(game.calculate_score(game.KNIFFEL), 50)

    def test_calculate_bonus(self):

        game = KniffelGame()

        player = "dummy_player"

        game.add_player(player)

        game._set_new_round(player)

        upper_section_score = 0
        # Assign highest value to every category on the upper section
        for dice_value, category in enumerate(game.categories[:6]):
            score = (dice_value + 1) * 5
            game._scores[player][category] = score
            upper_section_score += score

        # Force calculation
        game._score_bonus()

        self.assertEqual(game.my_score, upper_section_score + game.BONUS_VALUE)

        # Subtract the sixes
        upper_section_score -= game._scores[player][game.SIXES]
        game._scores[player][game.SIXES] = 0
        game._score_bonus()
        self.assertEqual(game.my_score, upper_section_score + game.BONUS_VALUE)

        # Subtract 3 fours so that it is exactly in the threshold
        upper_section_score -= 3 * 4
        game._scores[player][game.FOURS] -= 3 * 4
        game._score_bonus()
        self.assertEqual(game.my_score, upper_section_score + game.BONUS_VALUE)

        # Subtract 1 so that the bonus is not reached
        upper_section_score -= 1
        game._scores[player][game.ONES] -= 1
        game._score_bonus()
        self.assertEqual(game.my_score, upper_section_score)

    def test_score(self):

        game = KniffelGame()

        player = "dummy_player"

        game.add_player(player)

        game._set_new_round(player)
        game.roll()
        game._current_rolled_die = [2] * 5

        self.assertRaises(AssertionError, game.score, "SOME INVALID SCORE")

        game.score(game.KNIFFEL)
        self.assertEqual(game.my_score, 50)

        # Cannot repeat score
        self.assertRaises(AssertionError, game.score, game.KNIFFEL)

        # Nothing rolled
        self.assertRaises(AssertionError, game.score, game.ONES)

        game._current_rolled_die = [1] * 4 + [3]
        game.score(game.ONES)
        self.assertEqual(game.my_score, 54)

        game._current_rolled_die = [2] * 5
        game.score(game.TWOS)
        self.assertEqual(game.my_score, 54 + 100 + 2*5)
