from Game.GameState import GameState
from typing import List
import torch.nn.functional as F
import torch

RAF = -2
RBF = -1
BAF = 2
BBF = 1

FIRED_VALUE = 4

PAIRS = [[BBF, RAF], [BAF, RBF], [BAF, RAF], [BAF, BBF], [RAF, RBF]]
REVERSED_PAIRS = [[b, a] for a, b in PAIRS]


class KernelFeatureExtractor:
    def __init__(self):
        self.v_kernels = self.get_vertical_kernels()
        self.h_kernels = self.get_horizontal_kernels()
        self.d_kernels = self.get_diagonal_kernels()

    def get_kernels(self):
        '''
        kernels should output 4 if fired

        BA -> 2
        BB -> 1
        RA -> -2
        RB -> -1

        [R,B]

        [R,
         B]

        [R,0,
         0,B]

        [B,0,
         0,R]

        + color inversion
        + different layer pairs:

        blue-base - red-active
        blue-active - red-base
        blue-active - red-active
        red-active - blue-base
        red-active - blue-active


        :return: 40 kernels (4*2*5) some of unstandart form. So need to break into multiple functions(
        '''
        pass

    def get_horizontal_kernels(self):
        res = torch.unsqueeze(torch.tensor(PAIRS + REVERSED_PAIRS, requires_grad=False), 2)
        res.unsqueeze_(1)
        return res.float()

    def get_vertical_kernels(self):
        res = torch.unsqueeze(torch.tensor(PAIRS + REVERSED_PAIRS, requires_grad=False), 1)
        res.unsqueeze_(1)
        return res.float()

    def get_diagonal_kernels(self):
        '''
        :return:     20 diagonal kernels
        '''
        kernels = []
        for a, b in PAIRS + REVERSED_PAIRS:
            kernels.append([[0, a],
                            [b, 0]])
            kernels.append([[a, 0],
                            [0, b]])

        return torch.unsqueeze(torch.tensor(kernels, requires_grad=False), 1).float()

    def get_features(self, games):
        # move
        move_feature = torch.tensor([game.to_move for game in games], requires_grad=False).to(torch.int8)
        move_feature.unsqueeze_(1)

        fields = torch.tensor([game.field for game in games], requires_grad=False)
        fields_count = fields.shape[0]

        # positions of all types
        plain_features = torch.cat((fields == 2, fields == 1, fields == -1, fields == -2), dim=1).to(torch.int8)

        # 2x2 kernels
        fields = fields.reshape(-1, games[0].size_h, games[0].size_w)

        fields.unsqueeze_(1)  # channels = 1
        fields = fields.float()

        kernel_features = torch.cat((F.conv2d(fields, self.v_kernels).view(fields_count, -1),
                                     F.conv2d(fields, self.h_kernels).view(fields_count, -1),
                                     F.conv2d(fields, self.d_kernels).view(fields_count, -1)), dim=1) == 4
        kernel_features = kernel_features.to(torch.int8)
        features = torch.cat((move_feature, plain_features, kernel_features), dim=1)
        return features
