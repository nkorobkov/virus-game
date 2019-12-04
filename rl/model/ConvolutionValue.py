import torch.nn
import torch.nn.functional as F

from policy.RandomPolicy import RandomPolicy
from rl.feature.PlainFearutesExtractor import PlainFeatureExtractor

INTERESTING_STATES_COUNT = 4


class ConvolutionValue(torch.nn.Module):

    def __init__(self, field_h, field_w):
        super(ConvolutionValue, self).__init__()

        self.name = 'Convolution'

        self.field_h = field_h
        self.field_w = field_w

        self.conv1_size = 32
        self.conv2_size = 64
        self.dense_size = 256
        self.dropout = torch.nn.Dropout(p=0.5)

        self.conv1 = torch.nn.Conv2d(INTERESTING_STATES_COUNT, self.conv1_size, (3, 3), padding=1, bias=False)
        self.bn1 = torch.nn.BatchNorm2d(self.conv1_size)

        self.conv2 = torch.nn.Conv2d(self.conv1_size, self.conv2_size, (3, 3), padding=1, bias=False)
        self.bn2 = torch.nn.BatchNorm2d(self.conv2_size)

        self.fc1 = torch.nn.Linear(self.conv2_size * self.field_w * self.field_h, self.dense_size, bias=False)
        self.fc_bn1 = torch.nn.BatchNorm1d(self.dense_size)

        self.out = torch.nn.Linear(self.dense_size, 1)

    def forward(self, x):
        s = F.relu(self.bn1(self.conv1(x)))
        s = F.relu(self.bn2(self.conv2(s)))
        s = s.view(-1, self.conv2_size * self.field_w * self.field_h)
        s = self.dropout(F.relu(self.fc_bn1(self.fc1(s))))

        #  finally doing tanh to get value
        out = torch.tanh(self.out(s))
        return out


if __name__ == '__main__':
    from rl.learning.DataSampler import DataSampler

    feature_extractor = PlainFeatureExtractor()
    data_sampler = DataSampler(feature_extractor)
    features, labels = data_sampler.sample_data_by_self_play_with_policy(RandomPolicy(), 5, 5, 5, True)

    model = ConvolutionValue(5, 5)
    print(features.shape)
    features = features.float()
    a = model.forward(features)
    print(a.shape)
    print()
    print(a.median())
    print(a.mean())
    print(a.std())
    print(a.max())
    print(a.min())

