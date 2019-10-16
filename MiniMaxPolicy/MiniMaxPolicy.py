from Policy.Policy import Policy
from Game.GameState import GameState
from MiniMaxPolicy.Evaluator import Evaluator


class MiniMaxPolicy(Policy):

    def __init__(self, evaluator: Evaluator, depth=3):
        self.evaluator: Evaluator = evaluator
        self.depth = depth

    def get_move(self, game_state: GameState):
        pass
