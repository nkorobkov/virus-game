import timeit
import tracemalloc
import cProfile
from Game.const import CellStates

BASIC_SETUP = '''
from Game.GameState import GameState, Field, Mask
from Game.const import CellStates, Teams, Position
from MiniMaxPolicy.Evaluator.SimpleEvaluators import ColoredCellsCountEvaluator, MovableCountEvaluator
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy

evaluator = MovableCountEvaluator()
policy = MiniMaxPolicy(evaluator, 1)
    '''
FIELD_INTRO = '''
field: Field = '''


def setup_for_field(field, h, w):
    setup = BASIC_SETUP + FIELD_INTRO + field + '''     
game = GameState.from_field_list({},{},field,Teams.BLUE)'''.format(h, w)
    return setup


def test_field(field, h, w, mes=''):
    t = timeit.timeit('policy.get_move(game)', setup=setup_for_field(field, h, w), number=10)
    print("field {} took {:.3}".format(mes.zfill(20).replace('0', ' '), t))

    return t


fieldCenter = '''[CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA]'''
'''
w\h |   0 |   1 |   2 |   3 |   4 |   5 |   6 |   7 |   8 |
=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+
   0 |  ♚  |     | ♚♚♚ |     |     |  ♚  |     | ♚♚♚ |  ♚  |
     |     |     | ♚♚♚ |     |     |     |     | ♚♚♚ |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   1 |     | ♘♘♘ |     |  ♚  | ♚♚♚ |     | ♚♚♚ |     |     |
     |     | ♘♘♘ |     |     | ♚♚♚ |     | ♚♚♚ |     |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   2 |     |     | ♘♘♘ |     |     | ♘♘♘ |     | ♚♚♚ |     |
     |     |     | ♘♘♘ |     |     | ♘♘♘ |     | ♚♚♚ |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   3 |     | ♚♚♚ |     | ♘♘♘ | ♘♘♘ |     | ♚♚♚ |     |     |
     |     | ♚♚♚ |     | ♘♘♘ | ♘♘♘ |     | ♚♚♚ |     |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   4 | ♘♘♘ |  ♚  |     | ♘♘♘ |     | ♘♘♘ | ♚♚♚ |     |     |
     | ♘♘♘ |     |     | ♘♘♘ |     | ♘♘♘ | ♚♚♚ |     |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   5 |     |  ♚  |     | ♘♘♘ | ♚♚♚ |     |     | ♚♚♚ |     |
     |     |     |     | ♘♘♘ | ♚♚♚ |     |     | ♚♚♚ |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   6 |  ♚  |     | ♘♘♘ | ♘♘♘ | ♚♚♚ |     |     |  ♘  |     |
     |     |     | ♘♘♘ | ♘♘♘ | ♚♚♚ |     |     |     |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   7 |     | ♚♚♚ |     |     |  ♘  |     |  ♘  |  ♘  |     |
     |     | ♚♚♚ |     |     |     |     |     |     |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
   8 |     |     |     |     |     |     |     |     |  ♘  |
     |     |     |     |     |     |     |     |     |     |
-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

'''
fieldReal = '''[CellStates.RA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.RB, CellStates.RA,
             CellStates.EE, CellStates.BB, CellStates.EE, CellStates.RA, CellStates.RB, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.RB, CellStates.EE,
             CellStates.EE, CellStates.RB, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.BB, CellStates.RA, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE,
             CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.RB, CellStates.EE,
             CellStates.RA, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE,
             CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.BA, CellStates.BA, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BA]
'''

res = []

res.append(test_field(fieldCenter, 7, 7, 'Simple center'))
res.append(test_field(fieldReal, 9, 9, 'Real Game'))


print()
print('{} tests took {:.3} secs'.format(len(res), sum(res)))
print()

cProfile.run('timeit.timeit(\'policy.get_move(game)\', setup=setup_for_field(fieldReal, 9,9), number=10)')
