from Engine.Engine import Engine
from Game.GameState import GameState
from MiniMaxEngine.Policy import Policy


class MiniMaxEngine(Engine):

    def __init__(self, policy: Policy, depth=3):
        self.policy: Policy = policy
        self.depth = depth

    def get_move(self, game_state: GameState):
        pass
