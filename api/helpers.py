import json
from game.GameState import GameState


def get_game_state_from_json(text_data_json) -> GameState:
    field = text_data_json["field"]
    size_h = text_data_json["sizeH"]
    size_w = text_data_json["sizeW"]
    to_move = text_data_json["toMove"]
    game_state = GameState.from_field_list(
        h=size_h, w=size_w, field=field, to_move=to_move
    )
    return game_state
