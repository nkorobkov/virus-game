from Policy.Policy import Policy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.Evaluator.SimpleEvaluators import MovableCountEvaluator, ColoredCellsCountEvaluator
from Game.GameState import GameState
from Policy.exceptions import *
from Game.const import *

import cProfile



def compare_deterministic_policies(policy1: Policy, policy2: Policy) -> float:
    fpw = int(play_game_between_policies(policy1, policy2, 9, 9, show=True))
    fpw += int(not play_game_between_policies(policy2, policy1, 9, 9, show=True))

    return fpw


def play_game_between_policies(policy1: Policy, policy2: Policy, h=9, w=9, show=False, show_steps=False) -> bool:
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
            winning_team = e.for_team.other
            break
        move_count += 1

    str_tmp = 'Winner is {} (playing for {}), in {} moves'
    if winning_team == Teams.BLUE:
        print(str_tmp.format(policy1.name, CellStates.BLUE_BASE.symbol, move_count))
    else:
        print(str_tmp.format(policy2.name, CellStates.RED_BASE.symbol, move_count))

    if show:
        game.print_field()
    return winning_team == Teams.BLUE


def move(game: GameState, policy: Policy, show_steps: bool):
    move = policy.get_move(game)
    game.make_move(move)
    if show_steps:
        game.print_field()
        print('policy {} checked {} positions to come up with that'.format(policy.name, policy.pos_checked))
        print()


if __name__ == '__main__':
    evaluatorActiveCells = ColoredCellsCountEvaluator()
    evaluatorMoveCount = MovableCountEvaluator()

    policyMC = MiniMaxPolicy(evaluatorMoveCount, 2)
    policyAC = MiniMaxPolicy(evaluatorActiveCells, 2)

    print(compare_deterministic_policies(policyMC, policyAC))

    #play_game_between_policies(policy2,policy1, 9, 9, True, True)
    #cProfile.run(
        #'compare_deterministic_policies(policy1, policy2)')

