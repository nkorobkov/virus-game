from game.GameState import GameState


class Evaluator:
    name = "baseclass"

    def evaluate(self, game_state: GameState) -> float:
        raise NotImplementedError()
