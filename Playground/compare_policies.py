from Policy.Policy import Policy
from Policy.RandomPolicy import RandomPolicy
from Game.GameState import GameState
from Policy.exceptions import *


def compare_policies(policy1: Policy, policy2: Policy) -> float:
    first_policy_won_count = 0
    n = 100

    for i in range(n):
        fpw = play_game_between_policies(policy1, policy2)
        if fpw:
            first_policy_won_count +=1
    return first_policy_won_count/n


def play_game_between_policies(policy1: Policy, policy2: Policy, show=False) -> bool:
    '''
    plays a game between policy1 and policy2
    :param policy1:
    :param policy2:
    :param show: print field after moves
    :return: bool --> did policy1 won
    '''
    game = GameState(10, 10)
    move_count = 0
    while True:
        try:
            move1 = policy1.get_move(game)
            game.make_move(move1)
            if show:
                game.print_field()
        except NoValidMovesException:
            first_policy_won = False
            break

        try:
            move2 = policy2.get_move(game)
            game.make_move(move2)
            if show:
                game.print_field()
        except NoValidMovesException:
            first_policy_won = True
            break
        move_count += 1
    print('Winner is {}, in {} moves'.format(policy1.__class__ if first_policy_won else policy2.__class__, move_count))
    return first_policy_won


if __name__ == '__main__':
    policy1 = RandomPolicy()
    policy2 = RandomPolicy()

    print(compare_policies(policy1, policy2))