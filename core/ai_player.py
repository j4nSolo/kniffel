"""

AI Player Base shall be able to interact with the game in the following ways (actions):
- save die (1 or more) from both the already previously saved and the newly rolled ones
- roll the unsaved die
- score category taking into account both rolled and saved die

"""


class AIPlayerBase(object):

    def round(self, game):
        raise NotImplementedError
