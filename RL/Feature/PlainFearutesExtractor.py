import torch
from RL.Feature.FeatureExtractor import FeatureExtractor


class PlainFeatureExtractor(FeatureExtractor):

    def get_features(self, games):
        # returns field features only with blue to move assumption

        move_feature = torch.tensor([game.to_move for game in games], requires_grad=False).to(torch.int8)
        h, w = games[0].size_h, games[0].size_w
        fields = torch.tensor([game.field for game in games], requires_grad=False)

        # filp fields with red moving to have blue move from top corner
        fields_to_flip = move_feature == -1
        fields[fields_to_flip] = -fields[fields_to_flip].flip(1)

        # positions of all types
        plain_features = torch.cat((fields == 2, fields == 1, fields == -1, fields == -2), dim=1).to(torch.int8)

        # features shape = batch_size,layers=4,h,w
        return plain_features.reshape(len(games), 4, h, w)


if __name__ == '__main__':
    from Game.GameState import GameState

    game1 = GameState(3, 3)
    game2 = GameState(3, 3)
    game2.make_move(next(game2.get_all_moves()))

    pfe = PlainFeatureExtractor()
    r = pfe.get_features([game1, game2])
    print(r.shape)
    print(r)
