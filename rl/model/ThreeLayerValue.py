import torch.nn
import torch.nn.functional as F
INTERESTING_STATES_COUNT = 4

HORIZONTAL_KERNELS_COUNT = 5 * 2
VERTICAL_KERNELS_COUNT = 5 * 2
DIAGONAL_KERNELS_COUNT = 5 * 4


class ThreeLayerValue(torch.nn.Module):

    def __init__(self, field_h, field_w, hidden_size_1 = 128, hidden_size_2 = 64, hidden_size_3=32):
        super(ThreeLayerValue, self).__init__()

        self.name = 'Single Layered model for game value on kernel features'

        self.field_h = field_h
        self.field_w = field_w
        self.hidden_size_1 = hidden_size_1
        self.hidden_size_2 = hidden_size_2
        self.hidden_size_3 = hidden_size_3

        self.plain_features_weights_count = field_h * field_w * INTERESTING_STATES_COUNT

        self.input_size = self.plain_features_weights_count + \
                          field_h * (field_w - 1) * HORIZONTAL_KERNELS_COUNT + \
                          (field_h - 1) * field_w * VERTICAL_KERNELS_COUNT + \
                          (field_h - 1) * (field_w - 1) * DIAGONAL_KERNELS_COUNT

        self.net = torch.nn.Sequential(
            torch.nn.Linear(self.input_size, self.hidden_size_1),
            torch.nn.BatchNorm1d(self.hidden_size_1),  # applying batch norm
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(self.hidden_size_1, self.hidden_size_2),
            torch.nn.BatchNorm1d(self.hidden_size_2),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(self.hidden_size_2, self.hidden_size_3),
            torch.nn.BatchNorm1d(self.hidden_size_3),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(self.hidden_size_3, 1),
            torch.nn.Tanh()
        )

        #self.dropout = torch.nn.Dropout(p=0.5)


    def forward(self, x):


        return self.net(x)
