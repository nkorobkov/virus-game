from typing import Callable
from Game.GameState import GameState

Policy = Callable[[GameState], float]


def trivial_policy(game_state: GameState) -> float:
    return game_state.to_move.value
