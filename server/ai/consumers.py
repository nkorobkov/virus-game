import os

import torch
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json

from minimax_policy.MiniMaxPolicy import MiniMaxPolicy
from minimax_policy.ModelGuidedMiniMax import ModelGuidedMiniMax
from policy.ModelTreeD2Policy import ModelTreeD2Policy
from server.main.settings import BASE_DIR

from minimax_policy.evaluator.SimpleEvaluators import ActiveCountEvaluator
from game.GameState import GameState
from policy.ModelBasedPolicy import ModelBasedPolicy
from rl.feature.PlainFearutesExtractor import PlainFeatureExtractor
from rl.model.ConvolutionValue import ConvolutionValue
from pprint import pprint
import asgiref.sync


class AIConsumer(AsyncWebsocketConsumer):

    async def disconnect(self, close_code):
        del self.engine

    async def receive(self, text_data):
        # todo add fail safety
        text_data_json = json.loads(text_data)

        field = text_data_json['field']
        size_h = text_data_json['sizeH']
        size_w = text_data_json['sizeW']
        to_move = text_data_json['toMove']
        game_state = GameState.from_field_list(h=size_h, w=size_w, field=field, to_move=to_move)
        print('state received, finding a move')
        move = await asgiref.sync.sync_to_async(self.engine.get_move)(game_state)
        await self.send(text_data=json.dumps({
            'move': move
        }))
        print('move sent')


class TonyAIConsumer(AIConsumer):
    async def connect(self):
        self.h, self.w = 8, 8
        model = ConvolutionValue(self.h, self.w)
        state_dict = await asgiref.sync.sync_to_async(torch.load)(
            os.path.join(BASE_DIR, 'ai/trained_models/conv8value.pt'))
        model.load_state_dict(state_dict)
        feature_extractor = PlainFeatureExtractor()
        self.engine = ModelBasedPolicy(model, feature_extractor, self.h, self.w)
        await self.accept()


class JessieAIConsumer(AIConsumer):
    async def connect(self):
        self.h, self.w = 8, 8
        model = ConvolutionValue(self.h, self.w)
        state_dict = await asgiref.sync.sync_to_async(torch.load)(
            os.path.join(BASE_DIR, 'ai/trained_models/conv8value.pt'))
        model.load_state_dict(state_dict)
        feature_extractor = PlainFeatureExtractor()
        evaluatorActiveCells = ActiveCountEvaluator()

        self.engine = ModelGuidedMiniMax(model,
                                         feature_extractor,
                                         self.h,
                                         self.w,
                                         evaluatorActiveCells,
                                         lambda x: 30,
                                         depth=3)
        await self.accept()


class MaxAIConsumer(AIConsumer):
    async def connect(self):
        evaluator = ActiveCountEvaluator()
        self.engine = MiniMaxPolicy(evaluator, 2)
        await self.accept()
       