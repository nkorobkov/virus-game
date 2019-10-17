from Policy.Policy import Policy
from Policy.RandomPolicy import RandomPolicy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.Evaluator.SimpleEvaluators import MovableCountEvaluator, BasesCountEvaluator
from Game.GameState import GameState
from Policy.exceptions import *
from Game.const import *


def compare_policies(policy1: Policy, policy2: Policy) -> float:
    first_policy_won_count = 0
    n = 100

    for i in range(n):
        fpw = play_game_between_policies(policy1, policy2, show=True)
        if fpw:
            first_policy_won_count += 1
    return first_policy_won_count / n


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
    evaluator = BasesCountEvaluator()
    policy1 = MiniMaxPolicy(evaluator, 2)
    policy2 = MiniMaxPolicy(evaluator, 1)

    play_game_between_policies(policy1, policy2, 8, 8, True, True)

    print(compare_policies(policy1, policy2))
