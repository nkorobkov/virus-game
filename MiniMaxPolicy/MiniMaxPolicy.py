from Game.const import Teams
from Policy.Policy import Policy
from Game.GameState import GameState
from MiniMaxPolicy.Evaluator import Evaluator


class MiniMaxPolicy(Policy):

    def __init__(self, evaluator: Evaluator, depth=3):
        self.evaluator: Evaluator = evaluator
        self.depth = depth
        self.pos_checked = 0

    def get_move(self, game_state: GameState):
        self.pos_checked = 0
        if game_state.to_move == Teams.BLUE:
            return self.get_max(game_state, self.depth)[1]
        else:
            return self.get_min(game_state, self.depth)[1]

    def get_max(self, game_state, depth):
        return self.get_smth(game_state, depth, lambda x,y: x>y, self.get_min, -1000)

    def get_min(self, game_state, depth):
        return self.get_smth(game_state, depth, lambda x,y: x<y, self.get_max, 1000)

    def get_smth(self, game_state, depth, func, recursive_func, existing_reward):
        if depth == 0:
            self.pos_checked +=1
            return self.evaluator.evaluate(game_state), None
        else:
            top_move = None
            for move in game_state.get_all_moves():
                reward, prev_move = recursive_func(game_state.get_copy_with_move(move), depth - 1)
                if func(reward, existing_reward):
                    existing_reward = reward
                    top_move = move
            return existing_reward, top_move
