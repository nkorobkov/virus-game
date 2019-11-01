import time

from Policy.Policy import EstimatingPolicy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.PartialMiniMaxPolicy import PartialMiniMaxPolicy
from MiniMaxPolicy.Evaluator.SimpleEvaluators import MovableCountEvaluator, ColoredCellsCountEvaluator
from MiniMaxPolicy.Evaluator.BidirectionalStepsWithWeightEval import BidirectionalStepsWithWeightEval
from Policy.ModelBasedPolicy import ModelBasedPolicy
from Game.GameState import GameState
from Policy.exceptions import *
from Game.CellStates import *
from RL.Model.LinearValue import LinearValue
import cProfile


def compare_deterministic_policies(policy1: EstimatingPolicy, policy2: EstimatingPolicy) -> float:
    fpw = int(play_game_between_policies(policy1, policy2, 9, 9, show=True))
    fpw += int(not play_game_between_policies(policy2, policy1, 9, 9, show=True))

    return fpw


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

    str_tmp = 'Winner is {} (playing for {}), in {} moves'
    if winning_team == Teams.BLUE:
        print(str_tmp.format(policy1.name, CellStates.symbol(CellStates.BLUE_BASE), move_count))
    else:
        print(str_tmp.format(policy2.name, CellStates.symbol(CellStates.RED_BASE), move_count))

    if show:
        game.print_field()
    return winning_team == Teams.BLUE


def move(game: GameState, policy: EstimatingPolicy, show_steps: bool):
    move = policy.get_move(game)
    game.make_move(move)
    if show_steps:
        game.print_field()
        print('policy {} checked {} positions to come up with that'.format(policy.name, policy.pos_checked))
        print()


if __name__ == '__main__':
    evaluatorActiveCells = ColoredCellsCountEvaluator()
    evaluatorMoveCount = MovableCountEvaluator()
    evaluatorBid = BidirectionalStepsWithWeightEval()

    policyMC = MiniMaxPolicy(evaluatorMoveCount, 1)
    policyAC = MiniMaxPolicy(evaluatorActiveCells, 2)
    policyBD = MiniMaxPolicy(evaluatorBid, 2)

    policy_partial_ac = PartialMiniMaxPolicy(evaluatorActiveCells, lambda x: 100, 4)

    model = LinearValue(9, 9)
    model_based_explore = ModelBasedPolicy(model, 9, 9, 0.1)
    model_based = ModelBasedPolicy(model, 9, 9)
    t = time.time()
    for _ in range(1):
        play_game_between_policies(model_based_explore, model_based, 9, 9, True)
        print(time.time() - t)
    # print(compare_deterministic_policies(policyAC, policyMC))

    cProfile.run('play_game_between_policies(model_based, model_based_explore, 9, 9,True)')
