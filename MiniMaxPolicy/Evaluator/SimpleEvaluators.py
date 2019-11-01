from Game.GameState import GameState
from MiniMaxPolicy.Evaluator.Evaluator import Evaluator


class MovableCountEvaluator(Evaluator):
    name = 'Movable count'

    def evaluate(self, game_state: GameState) -> float:
        '''
        It is not symmetrical!
        That is bad.
        :param game_state:
        :return:
        '''
        return game_state.to_move * (
                sum(game_state.get_all_single_moves_mask()[0]) / sum(game_state.movable_masks[game_state.to_move]))


class ColoredCellsCountEvaluator(Evaluator):
    name = 'active cells count'

    def evaluate(self, game_state: GameState) -> float:
        return sum(game_state.field) / len(game_state.field)
