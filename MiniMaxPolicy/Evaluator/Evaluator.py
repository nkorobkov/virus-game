from Game.GameState import GameState


class Evaluator:

    def evaluate(self, game_state: GameState) -> float:
        raise NotImplementedError()


class RandomEvaluator(Evaluator):

    def evaluate(self, game_state: GameState) -> float:
        return game_state.to_move.value
