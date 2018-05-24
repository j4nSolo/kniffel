

from core.game import KniffelGame


class Tournament(object):

    def __init__(self, no_games, players):

        self._games = [KniffelGame() for _ in range(no_games)]
        self._players = players

    def start(self):

        # Starting distribution: every player won 0 games so far
        winning_distribution = {player: 0 for player in self._players}

        max_score = 0
        # loop over all games
        for game in self._games:
            game.add_player(*self._players)
            game.play()

            print(list(game.total_scores.values()))

            # Get winner
            max_points = max(game.total_scores.values())
            max_score = max(max_score, max_points)
            winners = [player for player in game.players if game.total_scores[player] == max_points]
            for winner in winners:
                winning_distribution[winner] += 1

        print("Winning distribution out of {games_no} games: {distribution}".format(
            games_no=len(self._games),
            distribution=", ".join(("{player_name} won {won_games_no}".format(
                player_name=player_name, won_games_no=won_games_no
            ) for player_name, won_games_no in iter(winning_distribution.items())))
        ))
        print("Maximum score was {}".format(max_score))

