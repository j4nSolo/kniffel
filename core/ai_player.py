"""

AI Player Base shall be able to interact with the game in the following ways (actions):
- save die (1 or more) from both the already previously saved and the newly rolled ones
- roll the unsaved die
- score category taking into account both rolled and saved die

"""


class AIPlayerBase(object):

    def __init__(self, name):

        self._name = name

    def round(self, game):
        # Must be implemented on subclass
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return self.name
