import torch
from RL.Feature.FeatureExtractor import FeatureExtractor

class PlainFeatureExtractor(FeatureExtractor):

    def get_features(self, games):
        # move
        move_feature = torch.tensor([game.to_move for game in games], requires_grad=False).to(torch.int8)
        move_feature.unsqueeze_(1)

        fields = torch.tensor([game.field for game in games], requires_grad=False)

        # positions of all types
        plain_features = torch.cat((fields == 2, fields == 1, fields == -1, fields == -2), dim=1).to(torch.int8)

        features = torch.cat((move_feature, plain_features), dim=1)
        return features
