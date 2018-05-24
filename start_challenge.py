"""
This will start a challenge with all .pyc contained within the "players" directory.
 Requisite for all candidates is the definition of the following two properties within the module:
 __ai__ = "Name of your AI class"
 __ainame__ = "Name of your player"
 Example is available in sample.stupid_ai_player.py

By default the number of games played is 1000, but can be changed via the optional parameter '--games_no'. Example:
 python start_challenge --games_no=500
"""

GAMES_NO_DEFAULT = 1000
AI_NAME_PROP = '__ai_name__'
AI_CLASS_PROP = '__ai_class__'

if __name__ == '__main__':

    from core.tournament import Tournament
    from argparse import ArgumentParser

    import players

    parser = ArgumentParser()
    parser.add_argument("--games_no", help="Amount of games to be played", default=GAMES_NO_DEFAULT)
    args = parser.parse_args()

    ais = dict()
    for module in players.__all__:
        mod = __import__('players.' + module, fromlist=[AI_CLASS_PROP, AI_NAME_PROP])
        try:
            ai_name = getattr(mod, AI_NAME_PROP)
            ai_class = getattr(mod, AI_CLASS_PROP)
            ais.update({ai_name: getattr(mod, ai_class)})
            print("Player AI found with name '%s'" % ai_name)
        except AttributeError:
            continue

    players = [ai(ai_name) for ai_name, ai in ais.iteritems()]

    tournament = Tournament(int(args.games_no), players)
    tournament.start()
