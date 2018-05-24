"""
Stupid player. Just rolls once and tries to score it in the first possible category. Good results!!!
"""

from core.ai_player import AIPlayerBase

# Properties for this AI
__ai_class__ = "StupidAIPlayer"
__ai_name__ = "Stupid"


class StupidAIPlayer(AIPlayerBase):

    def __init__(self, name):

        super(StupidAIPlayer, self).__init__(name=name)

    def round(self, game):

        # Roll die. Don't give a shit about the outcome.
        game.roll()

        category = 0
        while True:
            try:
                # Try to score on the category
                game.score(game.categories[category])
                # Break once the player has scored
                break
            except AssertionError:
                # Thrown when the category had a score already. Then, he moves to the next category and tries it again.
                category += 1


if __name__ == '__main__':

    from core.tournament import Tournament

    players = [
        StupidAIPlayer("Jandro"),
        StupidAIPlayer("Sven"),
        StupidAIPlayer("Mark"),
        StupidAIPlayer("Sebastian"),
        StupidAIPlayer("Ralf"),
    ]

    tournament = Tournament(500, players)
    tournament.start()
