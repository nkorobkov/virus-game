from MiniMaxPolicy.Evaluator.SimpleEvaluators import *
from MiniMaxPolicy.MiniMaxPolicy import *
from Game.GameState import GameState, Field
from Game.const import *
from Test.Policy.BaseCasesTestPolicy import BaseCasesTests
import unittest


class TestMimiMaxBasic(BaseCasesTests.TestPolicyBasics):
    def setUp(self):
        evaluator = ColoredCellsCountEvaluator()
        self.policy = MiniMaxPolicy(evaluator, 1)

