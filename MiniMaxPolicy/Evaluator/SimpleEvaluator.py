from Game.GameState import GameState
from MiniMaxPolicy.Evaluator.Evaluator import Evaluator


class SimpleEvaluator(Evaluator):

    def evaluate(self, game_state: GameState) -> float:
        return game_state.to_move.value * (sum(game_state.get_all_single_moves_mask()[0])/len(game_state.field))
