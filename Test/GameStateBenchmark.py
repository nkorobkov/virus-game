import timeit
import tracemalloc
import cProfile



BASIC_SETUP = '''
from Game.GameState import GameState, Field, Mask
from Game.const import CellStates, Teams, Position
    
    '''
FIELD_INTRO = '''
field: Field = '''


def setup_for_field(field, h, w):
    setup = BASIC_SETUP + FIELD_INTRO + field + '''     
game = GameState.from_field_list({},{},field,Teams.BLUE)'''.format(h, w)
    return setup


def test_field(field, h, w, mes=''):
    t = timeit.timeit('game.get_all_moves()', setup=setup_for_field(field, h, w), number=1000)
    print("field {} took {:.3}".format(mes.zfill(20).replace('0',' '), t))

    return t

fieldCenter = '''[CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE]'''

fieldLayered = '''[CellStates.BA, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.BB, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
             CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.EE,
             CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE]'''

fieldRandomBases = '''[CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
         CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
         CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE,
         CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB]'''


fieldMaxAccessible = '''\
[CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB,
CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE,
CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE]'''


fieldTotalBases = '''\
[CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB,
CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.EE, CellStates.EE,
CellStates.BB, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.BB]'''

fieldLayeredBigBases = '''\
[CellStates.BA, CellStates.RB, CellStates.RB, CellStates.RB, CellStates.RB, CellStates.RB, CellStates.RB,
CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB, CellStates.BB,
CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.EE]'''

res = []


res.append(test_field(fieldCenter, 7, 7, 'Simple center'))
res.append(test_field(fieldLayered, 7, 7, 'fieldLayered'))
res.append(test_field(fieldRandomBases, 7, 7, 'fieldRandomBases'))
res.append(test_field(fieldMaxAccessible, 7, 7, 'fieldMaxAccessible'))
res.append(test_field(fieldTotalBases, 7, 7, 'fieldTotalBases'))
res.append(test_field(fieldLayeredBigBases, 14, 7, 'fieldLayeredBigBases'))


print()
print('{} tests took {:.3} secs'.format(len(res), sum(res)))
print()

cProfile.run('timeit.timeit(\'game.get_all_moves()\', setup=setup_for_field(fieldLayeredBigBases, 14,7), number=1000)')

