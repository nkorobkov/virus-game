from Game.const import Teams
from Policy.Policy import Policy
from Game.GameState import GameState
from MiniMaxPolicy.Evaluator import Evaluator
from Policy.exceptions import *


class MiniMaxPolicy(Policy):

    def __init__(self, evaluator: Evaluator, depth=3):
        self.evaluator: Evaluator = evaluator
        self.depth = depth
        self.pos_checked = 0
        self.name = 'MiniMax with depth {} and evaluator {}'.format(depth, evaluator.name)

    def get_move(self, game_state: GameState):
        self.pos_checked = 0
        if game_state.to_move == Teams.BLUE:
            return self.get_max(game_state, self.depth)[1]
        else:
            return self.get_min(game_state, self.depth)[1]

    def get_max(self, game_state, depth, alpha=-1000, betta=1000):
        '''

        :param game_state:
        :param depth:
        :param alpha: Best already explored option for maximizing player (BLUE)
        :param betta: Best already explored option for Minimizing player (RED)
        :return:
        '''
        existing_reward = -1000
        if depth == 0:
            self.pos_checked += 1
            return self.evaluator.evaluate(game_state), None
        else:
            top_move = None

            for move in game_state.get_all_moves():
                reward, prev_move = self.get_min(game_state.get_copy_with_move(move), depth - 1, alpha, betta)
                if reward > existing_reward:
                    existing_reward = reward
                    top_move = move
                    if existing_reward > alpha:
                        # we have a nice guarantee here. If min search would try to produce smth worse, it could stop.
                        alpha = existing_reward
                    if existing_reward >= betta:
                        # we know that on previous move min player guarantied something better than this,
                        # so can stop searching
                        return existing_reward, top_move
            if top_move is None:
                if depth == self.depth:
                    raise NoValidMovesException(for_team=game_state.to_move)
                else:
                    return -100, None

        return existing_reward, top_move

    def get_min(self, game_state, depth, alpha=-1000, betta=1000):
        existing_reward = 1000
        if depth == 0:
            self.pos_checked += 1
            return self.evaluator.evaluate(game_state), None
        else:
            top_move = None
            for move in game_state.get_all_moves():
                reward, prev_move = self.get_max(game_state.get_copy_with_move(move), depth - 1, alpha, betta)
                if reward < existing_reward:
                    existing_reward = reward
                    top_move = move

                    if existing_reward < betta:
                        betta = existing_reward
                    if existing_reward <= alpha:
                        return existing_reward, top_move
            if top_move is None:
                if depth == self.depth:
                    raise NoValidMovesException(for_team=game_state.to_move)
                else:
                    return 100, None
            return existing_reward, top_move
