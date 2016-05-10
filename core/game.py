
from random import shuffle, randrange


class KniffelGame(object):

    def __init__(self):

        self._players = []
        self._current_saved_die = None
        self._current_rolled_die = None

    def add_player(self, player):
        self._players.append(player)

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

        return result

    def save(self, die):

        assert self._current_rolled_die is not None
        assert self._check_die_availability(die)

        self._current_saved_die = die

    # def score(self, ):

    @property
    def players(self):
        return self._players

    def _shuffle(self):
        shuffle(self._players)

    def _set_new_round(self):
        self._roll_times = 0
        self._current_saved_die = None
        self._current_rolled_die = None

    def _check_die_availability(self, die):

        die_set = self._current_rolled_die + self._current_saved_die if self._current_saved_die is not None else []

        try:
            for dice in die:
                die_set.remove(dice)
        except ValueError:
            return False

        return True

    def _wind_up(self):
        # TODO
        pass
