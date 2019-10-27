from Game.GameState import GameState
from collections import deque
from Game.const import CellStates
from MiniMaxPolicy.Evaluator.Evaluator import Evaluator
from typing import Deque

DEFAULT_REPRODUCTION_COST = 1
DEFAULT_KILL_COST = 1.2
DEFAULT_ACTIVE_BASE_COST = 0.8
DEFAULT_ACTIVE_CELL_COST = 0.6


class BidirectionalStepsWithWeightEval(Evaluator):
    name = 'steps for both sides with higher weight for step on enemy cell'

    def __init__(self, reproduction_cost=DEFAULT_REPRODUCTION_COST, kill_cost=DEFAULT_KILL_COST,
                 active_base_cost=DEFAULT_ACTIVE_BASE_COST, active_cell_cost=DEFAULT_ACTIVE_CELL_COST):

        self.reproduction_cost = reproduction_cost
        self.kill_cost = kill_cost
        self.active_base_cost = active_base_cost
        self.active_cell_cost = active_cell_cost

    def calc_all_active(self, active: Deque, team_value: int, game_state: GameState):
        seen = set()
        active_seen = set()
        result = 0
        active_size = len(active)
        while active:
            i = active.pop()
            for cell_i in game_state.get_cell_neighbours_indices(game_state.index_to_position(i)):
                state = game_state.field[cell_i].value
                if cell_i not in seen:
                    if state == 0:
                        # having available reproduction
                        seen.add(cell_i)
                        result += self.reproduction_cost
                    elif state == - team_value:
                        # having available kill
                        seen.add(cell_i)
                        result += self.kill_cost

                if state == team_value * 2 and cell_i not in active_seen:
                    result += self.active_base_cost
                    active_seen.add(cell_i)
                    active.append(cell_i)


        result += active_size * self.active_cell_cost
        return result

    def evaluate(self, game_state: GameState) -> float:
        '''
        Counts avaliable steps
        :param game_state:
        :return:
        '''
        active_positions = {1: deque(), -1: deque()}
        for i, cell in enumerate(game_state.field):
            cellv = cell.value
            if cellv == 1 or cellv == -1:
                active_positions[cellv].append(i)

        return self.calc_all_active(active_positions[1], 1, game_state) - \
               self.calc_all_active(active_positions[-1], -1, game_state)
