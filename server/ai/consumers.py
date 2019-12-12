import os

import torch
from channels.generic.websocket import WebsocketConsumer
import json
from server.main.settings import BASE_DIR


from game.GameState import GameState
from policy.ModelBasedPolicy import ModelBasedPolicy
from rl.feature.PlainFearutesExtractor import PlainFeatureExtractor
from rl.model.ConvolutionValue import ConvolutionValue

class AIConsumer(WebsocketConsumer):

    def disconnect(self, close_code):
        del self.engine

    def receive(self, text_data):
        # todo add fail safety
        text_data_json = json.loads(text_data)
        field = text_data_json['field']
        size_h = text_data_json['sizeH']
        size_w = text_data_json['sizeW']
        to_move = text_data_json['toMove']
        game_state = GameState.from_field_list(h=size_h, w=size_w, field=field, to_move=to_move)

        self.send(text_data=json.dumps({
            'move': self.engine.get_move(game_state)
        }))

        self.send(text_data=json.dumps({
            'move': self.engine.get_move(game_state)
        }))

class TonyAIConsumer(AIConsumer):
    def connect(self):
        self.h, self.w = 8, 8
        model = ConvolutionValue(self.h, self.w)
        print(BASE_DIR)
        model.load_state_dict(torch.load(os.path.join(BASE_DIR, 'ai/trained_models/conv8value.pt')))
        feature_extractor = PlainFeatureExtractor()
        self.engine = ModelBasedPolicy(model, feature_extractor, self.h, self.w)
        self.accept()

