

from core.game import KniffelGame


class Tournament(object):

    def __init__(self, no_games, players):

        self._games = [KniffelGame() for _ in range(no_games)]
        self._players = players

    def start(self):

        winning_distribution = {player: 0 for player in self._players}

        # loop over all games
        for game in self._games:
            game.add_player(*self._players)
            game.play()

            # Get winner
            max_points = max(game.total_scores.values())
            winners = [player for player in game.players if game.total_scores[player] == max_points]
            for winner in winners:
                winning_distribution[winner] += 1

        print(winning_distribution)

