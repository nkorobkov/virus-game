import timeit
import tracemalloc
import cProfile

BASIC_SETUP = '''
from Game.GameState import GameState, Field, Mask
from Game.const import CellStates, Teams, Position
from MiniMaxPolicy.Evaluator.SimpleEvaluators import ColoredCellsCountEvaluator
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy

evaluator = ColoredCellsCountEvaluator()
policy = MiniMaxPolicy(evaluator, 1)
    '''
FIELD_INTRO = '''
field: Field = '''


def setup_for_field(field, h, w):
    setup = BASIC_SETUP + FIELD_INTRO + field + '''     
game = GameState.from_field_list({},{},field,Teams.BLUE)'''.format(h, w)
    return setup


def test_field(field, h, w, mes=''):
    t = timeit.timeit('policy.get_move(game)', setup=setup_for_field(field, h, w), number=100)
    print("field {} took {:.3}".format(mes.zfill(20).replace('0', ' '), t))

    return t


fieldCenter = '''[CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA]'''

res = []

res.append(test_field(fieldCenter, 7, 7, 'Simple center'))


print()
print('{} tests took {:.3} secs'.format(len(res), sum(res)))
print()

cProfile.run('timeit.timeit(\'policy.get_move(game)\', setup=setup_for_field(fieldCenter, 7,7), number=100)')

