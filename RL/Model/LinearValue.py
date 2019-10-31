import torch.nn

INTERESTING_STATES_COUNT = 4

HORIZONTAL_KERNELS_COUNT = 5 * 2
VERTICAL_KERNELS_COUNT = 5 * 2
DIAGONAL_KERNELS_COUNT = 5 * 4


class LinearValue(torch.nn.Module):

    def __init__(self, field_h, field_w):
        super(LinearValue, self).__init__()

        self.name = 'Linear model for game value on kernel features'

        self.field_h = field_h
        self.field_w = field_w

        self.plain_features_weights_count = field_h * field_w * INTERESTING_STATES_COUNT

        self.input_size = 1 + \
                          field_h * field_w * INTERESTING_STATES_COUNT + \
                          field_h * (field_w - 1) * HORIZONTAL_KERNELS_COUNT + \
                          (field_h - 1) * field_w * VERTICAL_KERNELS_COUNT + \
                          (field_h - 1) * (field_w - 1) * DIAGONAL_KERNELS_COUNT

        self.linear = torch.nn.Linear(self.input_size, 1)
        self.init_weight_for_kernel_features()

    def init_weight_for_kernel_features(self):
        weight_for_move = torch.tensor([2.])
        weights_for_plain_features_blue = torch.zeros((self.plain_features_weights_count // 2)).normal_(1, 0.1)
        weights_for_plain_features_red = torch.zeros((self.plain_features_weights_count // 2)).normal_(-1, 0.1)
        weights_for_kernel_features = torch.zeros(self.input_size - 1 - self.plain_features_weights_count).normal_(0,
                                                                                                                   0.2)
        weights = torch.cat((weight_for_move,
                             weights_for_plain_features_blue,
                             weights_for_plain_features_red,
                             weights_for_kernel_features))
        weights.unsqueeze_(0)
        self.linear.weight = torch.nn.Parameter(weights)

    def forward(self, x):
        out = self.linear(x)
        return out
