from collections import OrderedDict
from random import shuffle, randrange
import collections


class KniffelGame(object):

    ONES = "ones"
    TWOS = "twos"
    THREES = "threes"
    FOURS = "fours"
    FIVES = "fives"
    SIXES = "sixes"
    THREE_X = "three of a kind"
    FOUR_X = "four of a kind"
    FULL_HOUSE = "full house"
    SMALL_STRAIGHT = "small straight"
    LARGE_STRAIGHT = "large straight"
    CHANCE = "chance"
    KNIFFEL = "kniffel"
    UPPER_BONUS = "upper bonus"
    KNIFFEL_BONUS = "kniffel bonus"

    BONUS_VALUE = 35
    UPPER_SECTION_MIN_SCORE_FOR_BONUS = sum(range(1, 7)) * 3  # = 63

    UPPER_SECTION = [ONES, TWOS, THREES, FOURS, FIVES, SIXES]

    categories = UPPER_SECTION + [
        THREE_X, FOUR_X, FULL_HOUSE, SMALL_STRAIGHT, LARGE_STRAIGHT,
        CHANCE, KNIFFEL]

    def __init__(self):
        """
        Creates a new game with no players beforehand.
        """

        self._players = []
        self._current_saved_die = None
        self._current_rolled_die = None
        self._scores = OrderedDict()
        self._current_player = None
        self._roll_times = None

    def add_player(self, *players):
        for player in players:
            self._players.append(player)
            self._scores[player] = OrderedDict([(key, None) for key in self.categories + [self.UPPER_BONUS, self.KNIFFEL_BONUS]])
            self._scores[player][self.KNIFFEL_BONUS] = 0

    def play(self):
        rounds = len(self.categories)
        while rounds > 0:
            for player in self.players:
                self._set_new_round(player)
                player.round(self)

            rounds -= 1

        self._wind_up()

    def roll(self):

        self._roll_times += 1
        if self._roll_times > 3:
            raise Exception

        # Rolling
        dice_to_be_rolled = 5 - len(self._current_saved_die if self._current_saved_die is not None else [])
        assert dice_to_be_rolled > 0
        result = [randrange(1, 7) for _ in range(dice_to_be_rolled)]

        self._current_rolled_die = result

        return result

    def save(self, die):

        assert self._current_rolled_die is not None
        assert self._check_die_availability(die)

        self._current_saved_die = die

    def score(self, category):

        scores = self._scores[self._current_player]

        assert category in scores
        assert scores[category] is None

        previous_kniffel = scores[self.KNIFFEL] == 50
        scores[category] = self.calculate_score(category)
        kniffel = True if min(self.die) == max(self.die) else False

        # Kniffel bonus
        if previous_kniffel and kniffel:
            # Extra points for second kniffel
            scores[self.KNIFFEL_BONUS] += 100

        # Upper section bonus
        if all(score is not None for score in self.upper_section_scores.values()):
            self._score_bonus()

        # Reset
        self._reset()

    def calculate_score(self, category):

        die = self.die
        assert len(die) == 5
        kniffel = True if min(die) == max(die) else False
        kniffel_dice = die[0] if kniffel else None

        try:
            joker = self._scores[self._current_player].values()[kniffel_dice - 1] is not None
        except TypeError:
            joker = False

        if category == self.ONES:
            unit_value = 1
            return sum((value for value in die if value == unit_value))
        elif category == self.TWOS:
            unit_value = 2
            return sum((value for value in die if value == unit_value))
        elif category == self.THREES:
            unit_value = 3
            return sum((value for value in die if value == unit_value))
        elif category == self.FOURS:
            unit_value = 4
            return sum((value for value in die if value == unit_value))
        elif category == self.FIVES:
            unit_value = 5
            return sum((value for value in die if value == unit_value))
        elif category == self.SIXES:
            unit_value = 6
            return sum((value for value in die if value == unit_value))
        elif category == self.THREE_X:
            return 6*5 if joker else (
                sum(die) if any(repetitions >= 3 for repetitions in collections.Counter(die).values()) else 0)
        elif category == self.FOUR_X:
            return 6*5 if joker else (
                sum(die) if any(repetitions >= 4 for repetitions in collections.Counter(die).values()) else 0)
        elif category == self.FULL_HOUSE:
            return 25 if joker or {3, 2}.issubset(collections.Counter(die).values()) else 0
        elif category == self.SMALL_STRAIGHT:
            return 30 if joker or any(option.issubset(die) for option in [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]) \
                else 0
        elif category == self.LARGE_STRAIGHT:
            return 40 if joker or any(option.issubset(die) for option in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]) else 0
        elif category == self.CHANCE:
            return sum(die)
        elif category == self.KNIFFEL:
            return 50 if kniffel else 0

        raise Exception

    @property
    def scores(self):
        """
        All current player's scores per category
        :return: Dictionary with scores
        :rtype: dict(str, int|None)
        """
        return self._scores

    @property
    def total_scores(self):
        """
        Total scores per player
        :return: Dictionary with scores
        :rtype: dict(AIPlayerBase, int)
        """
        return {player: self._player_score(player) for player in self.players}

    @property
    def my_score(self):
        """
        Current player's total score
        :return: Total score
        :rtype: int
        """
        return self._player_score(self._current_player)

    @property
    def upper_section_scores(self):
        """
        Scores per category for the upper section
        :return: Dictionary of category:score
        :rtype: dict(str, int|None)
        """
        return {category: self._scores[self._current_player][category] for category in self.UPPER_SECTION}

    @property
    def die(self):

        try:
            return self._current_rolled_die + (self._current_saved_die if self._current_saved_die is not None else [])
        except TypeError:
            raise AssertionError

    @property
    def players(self):
        return self._players

    def _player_score(self, player):
        return sum(score for score in self._scores[player].values() if score is not None)

    def _shuffle(self):
        shuffle(self._players)

    def _set_new_round(self, player):
        self._reset()
        self._current_player = player

    def _reset(self):

        self._roll_times = 0
        self._current_saved_die = None
        self._current_rolled_die = None

    def _check_die_availability(self, die):

        die_set = self.die

        try:
            for dice in die:
                die_set.remove(dice)
        except ValueError:
            return False

        return True

    def _score_bonus(self):

        upper_section_score = sum(self.upper_section_scores.values())

        bonus = self.BONUS_VALUE if upper_section_score >= self.UPPER_SECTION_MIN_SCORE_FOR_BONUS else 0
        self.scores[self._current_player][self.UPPER_BONUS] = bonus

    def _wind_up(self):
        # print(self.total_scores)
        pass
