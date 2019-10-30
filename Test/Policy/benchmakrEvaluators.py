from Game.GameState import Field
from Game.CellStates import CellStates
from Game.Teams import Teams
from MiniMaxPolicy.Evaluator.SimpleEvaluators import *
from MiniMaxPolicy.Evaluator.BidirectionalStepsWithWeightEval import BidirectionalStepsWithWeightEval
from time import time
import cProfile


stepcount_ev = MovableCountEvaluator()
colored_cells_ev = ColoredCellsCountEvaluator()
bid_ev = BidirectionalStepsWithWeightEval()

evals = [stepcount_ev, colored_cells_ev, bid_ev]

field: Field = \
    [CellStates.RA, CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE,
     CellStates.RB, CellStates.RA,
     CellStates.EE, CellStates.BB, CellStates.EE, CellStates.RA, CellStates.RB, CellStates.EE, CellStates.RB,
     CellStates.EE, CellStates.EE,
     CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.EE, CellStates.BB, CellStates.EE,
     CellStates.RB, CellStates.EE,
     CellStates.EE, CellStates.RB, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.EE, CellStates.RB,
     CellStates.EE, CellStates.EE,
     CellStates.BB, CellStates.RA, CellStates.EE, CellStates.BB, CellStates.EE, CellStates.BB, CellStates.RB,
     CellStates.EE, CellStates.EE,
     CellStates.EE, CellStates.RA, CellStates.EE, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE,
     CellStates.RB, CellStates.EE,
     CellStates.RA, CellStates.EE, CellStates.BB, CellStates.BB, CellStates.RB, CellStates.EE, CellStates.EE,
     CellStates.BA, CellStates.EE,
     CellStates.EE, CellStates.RB, CellStates.EE, CellStates.EE, CellStates.BA, CellStates.EE, CellStates.BA,
     CellStates.BA, CellStates.EE,
     CellStates.EE, CellStates.EE, CellStates.RA, CellStates.EE, CellStates.EE, CellStates.EE, CellStates.RA,
     CellStates.EE, CellStates.BA]
game = GameState.from_field_list(9, 9, field, Teams.BLUE)


def measure_eval_time(evaluator: Evaluator, n=1000, game=game):
    start = time()
    for i in range(n):
        evaluator.evaluate(game)
    return time() - start


n = 1000
for ev in evals:
    t = measure_eval_time(ev, n=n)

    print('evaluator {} took {:.3} sec on {} evals'.format(ev.name, t, n))

cProfile.run('[bid_ev.evaluate(game) for _ in range(10000)]')

cProfile.run('[stepcount_ev.evaluate(game) for _ in range(10000)]')