import time

from Policy.ModelTreeD2Policy import ModelTreeD2Policy
from Policy.Policy import EstimatingPolicy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from MiniMaxPolicy.ModelGuidedMiniMax import ModelGuidedMiniMax
from MiniMaxPolicy.Evaluator.SimpleEvaluators import MovableCountEvaluator, ActiveCountEvaluator
from Policy.RandomPolicy import RandomPolicy
from MiniMaxPolicy.Evaluator.BidirectionalStepsWithWeightEval import BidirectionalStepsWithWeightEval
from Policy.ModelBasedPolicy import ModelBasedPolicy
from Game.GameState import GameState, Position
from Policy.exceptions import *
from Game.CellStates import *
from RL.Model.ConvolutionValue2 import ConvolutionValue2
from RL.Model.LinearValue import LinearValue
from RL.Model.SingleLayerValue import SingleLayerValue
from RL.Model.ThreeLayerValue import ThreeLayerValue
from RL.Model.ConvolutionValue import ConvolutionValue
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from Playground.util import readable_time_since
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
    model_old.load_state_dict(torch.load('../RL/learning/data/model8-conv-disc.pt'))
    model_old.eval()
    model_old = ModelBasedPolicy(model_old, PlainFeatureExtractor(), h, w, 0.1)



    model_new_3 = ConvolutionValue(h, w)
    model_new_3.load_state_dict(torch.load('../RL/learning/data/model8-conv-disc-14-ep-95.pt'))
    model_new_3.eval()
    model_3 = ModelBasedPolicy(model_new_3, PlainFeatureExtractor(), h, w, 0.1)

    model_new_6 = ConvolutionValue(h, w)
    model_new_6.load_state_dict(torch.load('../RL/learning/data/model8-conv-disc2-10iz10.pt'))
    model_new_6.eval()
    model_6 = ModelBasedPolicy(model_new_6, PlainFeatureExtractor(), h, w, 0.1)


    model_guided = ModelGuidedMiniMax(model_new_6, PlainFeatureExtractor(), h, w, evaluatorActiveCells, lambda x: 30,
                                      depth=3,
                                      exploration_rate=0.1)
    model_tree = ModelTreeD2Policy(model_new_6, PlainFeatureExtractor(), h, w, lambda x: 30, 0.1)

    evaluated = model_3
    compare_to = model_tree

    for i in range(5):
        compare_policies(model_tree, policyAC2_r, 5, h, w, True, False)

    # cProfile.run('compare_policies(evaluated, compare_to, 1, h, w, False, False)')
