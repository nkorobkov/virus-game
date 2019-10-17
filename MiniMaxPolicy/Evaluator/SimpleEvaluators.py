from Game.GameState import GameState
from Game.const import *
from MiniMaxPolicy.Evaluator.Evaluator import Evaluator
from collections import Counter


class MovableCountEvaluator(Evaluator):
    name = 'Movable count'

    def evaluate(self, game_state: GameState) -> float:
        '''
        It is not symmetrical!
        That is bad.
        :param game_state:
        :return:
        '''
        return game_state.to_move.value * (
                sum(game_state.get_all_single_moves_mask()[0]) / sum(game_state.movable_mask))


class BasesCountEvaluator(Evaluator):
    name = 'Bases count'

    def evaluate(self, game_state: GameState) -> float:
        c = Counter(game_state.field)
        return (c[CellStates.BLUE_BASE] * 2 +
                c[CellStates.BLUE_ACTIVE] -
                c[CellStates.RED_BASE] * 2 -
                c[CellStates.RED_ACTIVE]) / len(game_state.field)
