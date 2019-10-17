from Policy.Policy import Policy
from Policy.RandomPolicy import RandomPolicy
from Game.GameState import GameState
from Game.const import Position
from Playground.const import HELP
from Playground.exceptions import *
from Game.exceptions import *
from Policy.exceptions import *
from copy import deepcopy

def get_position_from_user_input(s):
    try:
        h, w = tuple(map(int, s.split(' ')))
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
        raise GameInterruptedBuUser
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


def play_with_policy(policy: Policy):
    h, w = 4,4
    game = GameState(h, w)

    print('play with policy {} started'.format(policy.__class__))
    print('You are in the top left corner')
    winner = 0
    while True:
        try:
            if not list(game.get_all_moves()):
                winner = -1
            do_user_move(game)
            print('Your move is accepted, now policy moves')
            do_policy_move(game, policy)
        except NoValidMovesException:
            winner = 1
            break
        except GameInterruptedBuUser:
            break

    print('Game is over, thanks.')
    if winner == 1:
        print('You won, congratulations.')
    elif winner == -1:
        print('You lost this time.')
    else:
        print('game was interrupted')

def do_policy_move(game_state: GameState, policy: Policy):
    move = policy.get_move(game_state)
    game_state.make_move(move)


if __name__ == "__main__":
    policy = RandomPolicy()
    play_with_policy(policy)