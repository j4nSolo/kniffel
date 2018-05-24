"""
Smart player. Just rolls once and tries to score it in the first possible category. Good results!!!
"""
from stupid_ai_player import StupidAIPlayer
from core.ai_player import AIPlayerBase

# Properties for this AI
__ai_class__ = "SmartAIPlayer"
__ai_name__ = "Smart"


class SmartAIPlayer(AIPlayerBase):

    def __init__(self, name):

        super(SmartAIPlayer, self).__init__(name=name)

    def round(self, game):
        """
        Method that gets called on each player's turn

        :param core.game.KniffelGame game: game instance
        """

        # Roll die. Don't give a shit about the outcome.
        game.roll()

        category = 0
        while True:
            try:
                category_string = game.categories[category]
                # Try to score on the category
                try:
                    while game.calculate_score(category_string) == 0:
                        game.roll()
                except Exception:
                    pass
                game.score(category_string)
                # Break once the player has scored
                break
            except AssertionError:
                # Thrown when the category had a score already. Then, he moves to the next category and tries it again.
                category += 1


class SmarterAIPlayer(AIPlayerBase):

    def __init__(self, name):

        super(SmarterAIPlayer, self).__init__(name=name)

    def round(self, game):
        """
        Method that gets called on each player's turn

        :param core.game.KniffelGame game: game instance
        """

        # Roll die. Don't give a shit about the outcome.
        game.roll()

        category = 0
        best_category, best_score = 0, 0
        while category < len(game.categories):
            category_string = game.categories[category]
            if game.scores[self][category_string] is None:
                # Try to score on the category
                score = game.calculate_score(category_string)
                best_score = max(best_score, score)
                best_category = category if best_score == score else best_category

            category += 1

        game.score(game.categories[best_category])


if __name__ == '__main__':

    from core.tournament import Tournament

    players = [
        SmarterAIPlayer("Jandro"),
        StupidAIPlayer("Sven"),
        StupidAIPlayer("Mark"),
        StupidAIPlayer("Sebastian"),
        SmartAIPlayer("Ralf"),
    ]

    tournament = Tournament(500, players)
    tournament.start()
