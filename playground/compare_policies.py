import time

import sys

from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from policy.ModelTreeD2Policy import ModelTreeD2Policy
from policy.Policy import EstimatingPolicy
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from minimax_policy.ModelGuidedMiniMax import ModelGuidedMiniMax
from minimax_policy.evaluator.SimpleEvaluators import MovableCountEvaluator, ActiveCountEvaluator
from policy.RandomPolicy import RandomPolicy
from minimax_policy.evaluator.BidirectionalStepsWithWeightEval import BidirectionalStepsWithWeightEval
from policy.ModelBasedPolicy import ModelBasedPolicy
from game.GameState import GameState, Position
from policy.exceptions import *
from game.CellStates import *
from rl.model.ConvolutionValue2 import ConvolutionValue2
from rl.model.LinearValue import LinearValue
from rl.model.SingleLayerValue import SingleLayerValue
from rl.model.ThreeLayerValue import ThreeLayerValue
from rl.model.ConvolutionValue import ConvolutionValue
from rl.feature.PlainFearutesExtractor import PlainFeatureExtractor
from playground.util import readable_time_since
import cProfile
import torch


def play_game_between_policies(policy1: EstimatingPolicy, policy2: EstimatingPolicy, h=9, w=9, show=False,
                               show_steps=False) -> bool:
    '''
    plays a game between policy1 and policy2
    :param policy1:
    :param policy2:
    :param h: field size
    :param w:
    :param show: print field after all moves
    :param show_steps: print field after each move
    :return: bool --> did policy1 won
    '''
    game = GameState(h, w)
    move_count = 0
    while True:
        try:
            move(game, policy1, show_steps)
            move(game, policy2, show_steps)
        except NoValidMovesException as e:
            winning_team = Teams.other(e.for_team)
            break
        move_count += 1

    if show:
        str_tmp = 'Winner is {} (playing for {}), in {} moves'
        if winning_team == Teams.BLUE:
            print(str_tmp.format(policy1.name, CellStates.symbol(CellStates.BLUE_BASE), move_count))
        else:
            print(str_tmp.format(policy2.name, CellStates.symbol(CellStates.RED_BASE), move_count))
        game.print_field()
    return winning_team == Teams.BLUE


def move(game: GameState, policy: EstimatingPolicy, show_steps: bool):
    value, move = policy.get_best_option(game)
    game.make_move(move)
    if show_steps:
        game.print_field()
        print('V = {}, policy {} checked {} positions to come up with that'.format(value, policy.name,
                                                                                   policy.pos_checked))
        print()


def compare_policies(evaluated: EstimatingPolicy, compare_to: EstimatingPolicy, n, h, w, show=False, show_steps=False):
    t = time.time()
    wins = 0
    for _ in range(n):
        wins += 0 if play_game_between_policies(compare_to, evaluated, h, w, show, show_steps) else 1
        wins += play_game_between_policies(evaluated, compare_to, h, w, show, show_steps)

    print('{} -- {}:{} -- {} evaluation took: {}'.format(evaluated.name, wins, n * 2 - wins, compare_to.name,
                                                         readable_time_since(t)))
    return wins


if __name__ == '__main__':
    evaluatorActiveCells = ActiveCountEvaluator()
    evaluatorMoveCount = MovableCountEvaluator()
    evaluatorBid = BidirectionalStepsWithWeightEval()

    policyMC = MiniMaxPolicy(evaluatorMoveCount, 1)
    policyAC = MiniMaxPolicy(evaluatorActiveCells, 1)
    policyAC2 = MiniMaxPolicy(evaluatorActiveCells, 2)
    policyAC2_r = ExplorativeMiniMaxPolicy(evaluatorActiveCells, 0.1, 2)

    policyBD = MiniMaxPolicy(evaluatorBid, 2)
    policy_random = RandomPolicy()

    h, w = 8, 8
    model_old = ConvolutionValue(h, w)
    model_old.load_state_dict(torch.load('../rl/learning/data/model8-conv-disc.pt'))
    model_old.eval()
    model_old = ModelBasedPolicy(model_old, PlainFeatureExtractor(), h, w, 0.1)



    model_new_2gen = ConvolutionValue(h, w)
    model_new_2gen.load_state_dict(torch.load('../rl/learning/data/model8-second-gen-conv-15-1.pt'))
    model_new_2gen.eval()
    model_2 = ModelBasedPolicy(model_new_2gen, PlainFeatureExtractor(), h, w, 0.1)

    model_new_6 = ConvolutionValue(h, w)
    model_new_6.load_state_dict(torch.load('../rl/learning/data/model8-conv-disc2-10iz10.pt'))
    model_new_6.eval()
    model_6 = ModelBasedPolicy(model_new_6, PlainFeatureExtractor(), h, w, 0.1)


    model_guided = ModelGuidedMiniMax(model_new_6, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 30,
                                      depth=3,
                                      exploration_rate=0.1)
    model_tree = ModelTreeD2Policy(model_new_6, PlainFeatureExtractor(), h, w, lambda x: 30, 0.1)
    model2_tree = ModelTreeD2Policy(model_new_2gen, PlainFeatureExtractor(), h, w, lambda x: 30, 0.1)


    wins = 0
    for i in range(25):
        wins += compare_policies(model_tree,policyAC2_r , 1, h, w, False, False)
    print(wins)
    # cProfile.run('compare_policies(evaluated, compare_to, 1, h, w, False, False)')
