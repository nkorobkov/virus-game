from Game.GameState import GameState, Field, Mask
from Game.const import CellStates, Teams, Position
from random import random
from pprint import pprint
import timeit

from itertools import combinations


def moves_sanity_check(a):
    move_set = set()
    f = True
    for e in a:
        if len(set(e)) != 3:
            print("move ", e)
            f = False
        move_set.add(tuple(sorted(e)))
    print('number returned ', len(a), 'unique', len(move_set))
    return len(move_set) == len(a) and f


field: Field = [CellStates.BA, CellStates.BA, CellStates.RA, CellStates.BA, CellStates.RB,
             CellStates.BA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.BA, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB,
             CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
             CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA,
                CellStates.BA, CellStates.BA, CellStates.RA, CellStates.BA, CellStates.RB,
                CellStates.BA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
                CellStates.BA, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB,
                CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
                CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA,

                CellStates.BA, CellStates.BA, CellStates.RA, CellStates.BA, CellStates.RB,
                CellStates.BA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
                CellStates.BA, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB,
                CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
                CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA,

                CellStates.BA, CellStates.BA, CellStates.RA, CellStates.BA, CellStates.RB,
                CellStates.BA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
                CellStates.BA, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB,
                CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
                CellStates.BB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.RA
                ]

game = GameState(10,10)
    #GameState.from_field_list(10,10, field, Teams.BLUE)

game.print_field()

single_moves_mask, a = game.get_all_single_moves_mask()

single_positions = game.get_single_moves_positions_from_mask(single_moves_mask)

#print(single_positions)

double_moves, second_to_firsts, first_to_seconds = \
    game.get_all_double_moves_from_single_moves(single_positions, single_moves_mask, a)

#pprint(double_moves)

t_step_moves = list(game.get_all_3_steps_moves(double_moves, single_moves_mask, a))

dd_step_moves = list(game.get_all_dd_steps_moves(first_to_seconds))

# here we got move with duplicate single in both
d_step_moves = list(game.get_all_ds_steps_moves(single_positions, second_to_firsts))

s_step_moves = list(combinations(single_positions, 3))

print(len(t_step_moves))
print(len(dd_step_moves))
print(len(d_step_moves))
print(len(s_step_moves))
print()
print(len(list(game.get_all_moves())))
print(276)
print(0)

# pprint(dd_step_moves)

moves_sanity_check(list(game.get_all_moves()))

print()

n55 = list(game.get_cell_neighbours_positions(Position(2, 1)))
bad_moves = []
for move in list(game.get_all_moves()):
    f = True
    for pos in move:
        if pos == Position(0,0):
            f = False

    if not f:
        bad_moves.append(move)
        print(move)

print('bm ', len(bad_moves))


# pprint(t_step_moves)

# expect C(8,3)


def generateRandomField(s):
    field = []

    for i in range(s ** 2):
        r = random()
        if r > 0.25:

            field.append(CellStates.EE)
        elif r > 0.1:
            field.append(CellStates.BA)
        else:
            field.append(CellStates.BB)
    return field.__str__()
