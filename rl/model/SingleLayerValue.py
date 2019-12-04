import torch.nn
import torch.nn.functional as F
INTERESTING_STATES_COUNT = 4

HORIZONTAL_KERNELS_COUNT = 5 * 2
VERTICAL_KERNELS_COUNT = 5 * 2
DIAGONAL_KERNELS_COUNT = 5 * 4


class SingleLayerValue(torch.nn.Module):

    def __init__(self, field_h, field_w, hidden_size = 50):
        super(SingleLayerValue, self).__init__()

        self.name = 'Single Layered model for game value on kernel features'

        self.field_h = field_h
        self.field_w = field_w
        self.hidden_size = hidden_size

        self.plain_features_weights_count = field_h * field_w * INTERESTING_STATES_COUNT

        self.input_size = self.plain_features_weights_count + \
                          field_h * (field_w - 1) * HORIZONTAL_KERNELS_COUNT + \
                          (field_h - 1) * field_w * VERTICAL_KERNELS_COUNT + \
                          (field_h - 1) * (field_w - 1) * DIAGONAL_KERNELS_COUNT

        self.linear = torch.nn.Linear(self.input_size, self.hidden_size)
        self.dropout = torch.nn.Dropout(p=0.3)

        self.out = torch.nn.Linear(self.hidden_size, 1)


    def forward(self, x):
        state = self.linear(x)
        state = self.dropout(state)
        state = F.relu(state)
        out = self.out(state)
        return out
