import sys

from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from policy.Policy import Policy
from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.evaluator.SimpleEvaluators import MovableCountEvaluator, ActiveCountEvaluator
from game.GameState import GameState, Position
from playground.util import HELP, readable_time_since
from playground.exceptions import *
from game.exceptions import *
from policy.exceptions import *
from copy import deepcopy
from time import time


def get_position_from_user_input(s):
    try:
        s = s.strip(' ')
        s = s.split(' ')
        s = list(filter(lambda x: x.isdigit(), s))
        h, w = tuple(map(int, s))
        return Position(h, w)
    except Exception:
        raise InputDoesNotContainPosition


def submit_user_step(step: Position, game_state: GameState):
    # not cool that I check conditions for change of state of game outside of gamestate class
    try:
        assert check_step_valid(step, game_state)
        game_state.transition_single_cell(step)
    except (ForbidenTransitionError, AssertionError):
        raise MoveToPositionIsImpossible(step)


def check_step_valid(step: Position, game_state: GameState):
    single_moves_positions = game_state.get_single_moves_positions_from_mask(game_state.get_all_single_moves_mask()[0])
    return step in single_moves_positions


def process_unusual_input(s):
    if s == 'help':
        print(HELP)
        return
    if s == 'exit':
        raise GameInterruptedByUser
    raise InputCanNotBeRecognized


def do_user_step(game_state: GameState, steps_left=3):
    print()
    game_state.print_field()
    print()
    print('Enter your step. You have {} left'.format(steps_left))
    user_input = input()
    try:
        position = get_position_from_user_input(user_input)
        submit_user_step(position, game_state)
        return position
    except InputDoesNotContainPosition:
        try:
            process_unusual_input(user_input)
            return False
        except InputCanNotBeRecognized:
            print('We failed to recognize your input, please try again or print "help" for help.')
            return False
    except MoveToPositionIsImpossible:
        print('Move to position you entered is impossible, please try again')
        return False


def do_user_move(game_state: GameState):
    test_state = deepcopy(game_state)
    move = []
    i = 0
    while i < 3:
        step = do_user_step(test_state, 3 - i)
        if step:
            i += 1
            move.append(step)

    game_state.make_move(move)


def do_user_first_move(game_state: GameState):
    test_state = deepcopy(game_state)
    step = False
    while not step:
        step = do_user_step(test_state, 1)
    # copied from GameState move
    game_state.transition_single_cell(step)
    game_state.to_move = Teams.other(game_state.to_move)
    game_state.movable_masks = game_state.get_movable_masks()


def play_with_policy(policy: Policy, h=9, w=9):
    game = GameState(h, w)

    print('play with policy {} started.'.format(policy.name))
    print('You are in the top left corner.')
    winner = 0
    do_user_first_move(game)
    while True:
        try:
            print()
            game.print_field()
            print()
            print('Your move is accepted, now {} moves.'.format(policy.name))
            t = time()
            do_policy_move(game, policy)
            print('Policy made a move in {} sec. It checked {} positions'.format(readable_time_since(t),
                                                                                 policy.pos_checked))
            if list(game.get_all_moves()):
                do_user_move(game)
            else:
                # Game state has no valid moves --> player lost.
                winner = -1
                game.print_field()
                break
        except NoValidMovesException:
            winner = 1
            break
        except GameInterruptedByUser:
            break

    print('Game is over, thanks.')
    if winner == 1:
        print('You won, congratulations.')
    elif winner == -1:
        print('You lost this time.')
    else:
        print('Game was interrupted.')


def do_policy_move(game_state: GameState, policy: Policy):
    move = policy.get_move(game_state)
    game_state.make_move(move)


if __name__ == "__main__":
    evaluator = ActiveCountEvaluator()
    policy = MiniMaxPolicy(evaluator, 2)
    play_with_policy(policy, 8, 8)
