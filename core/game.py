
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
    BIG_STRAIGHT = "big straight"
    CHANCE = "chance"
    KNIFFEL = "kniffel"
    possible_scores = [
        ONES, TWOS, THREES, FOURS, FIVES, SIXES,
        THREE_X, FOUR_X, FULL_HOUSE, SMALL_STRAIGHT, BIG_STRAIGHT,
        CHANCE, KNIFFEL]

    def __init__(self):

        self._players = []
        self._current_saved_die = None
        self._current_rolled_die = None
        self._scores = dict()
        self._current_player = None

    def add_player(self, player):
        self._players.append(player)
        self._scores[player] = {key: None for key in self.possible_scores}

    def play(self):
        rounds = 13
        while rounds > 0:
            for player in self.players:
                self._set_new_round()
                player.round(self)

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

        assert category in self._scores[self._current_player]
        self._scores[self._current_player][category] = self.calculate_score(category)

    def calculate_score(self, category):

        die = self.die
        kniffel = True if min(die) == max(die) else False

        if category == self.ONES:
            unit_value = 1
            return sum((value for value in die if value == unit_value)) if not kniffel else unit_value * 5
        elif category == self.TWOS:
            unit_value = 2
            return sum((value for value in die if value == unit_value)) if not kniffel else unit_value * 5
        elif category == self.THREES:
            unit_value = 3
            return sum((value for value in die if value == unit_value)) if not kniffel else unit_value * 5
        elif category == self.FOURS:
            unit_value = 4
            return sum((value for value in die if value == unit_value)) if not kniffel else unit_value * 5
        elif category == self.FIVES:
            unit_value = 5
            return sum((value for value in die if value == unit_value)) if not kniffel else unit_value * 5
        elif category == self.SIXES:
            unit_value = 6
            return sum((value for value in die if value == unit_value)) if not kniffel else unit_value * 5
        elif category == self.THREE_X:
            return 6*5 if kniffel else (
                sum(die) if any(repetitions >= 3 for repetitions in collections.Counter(die).values()) else 0)
        elif category == self.FOUR_X:
            return 6*5 if kniffel else (
                sum(die) if any(repetitions >= 4 for repetitions in collections.Counter(die).values()) else 0)

        raise Exception

    @property
    def die(self):

        return self._current_rolled_die + (self._current_saved_die if self._current_saved_die is not None else [])

    @property
    def players(self):
        return self._players

    def _shuffle(self):
        shuffle(self._players)

    def _set_new_round(self, player):
        self._roll_times = 0
        self._current_saved_die = None
        self._current_rolled_die = None
        self._current_player = player

    def _check_die_availability(self, die):

        die_set = self.die

        try:
            for dice in die:
                die_set.remove(dice)
        except ValueError:
            return False

        return True

    def _wind_up(self):
        # TODO
        pass
