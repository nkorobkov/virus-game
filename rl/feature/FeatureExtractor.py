from typing import List

from game.GameState import GameState


class FeatureExtractor:
    def get_features(self, games: List[GameState]):
        raise NotImplementedError('get_features  of  base class')
