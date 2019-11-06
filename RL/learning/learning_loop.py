# %%

import torch
import torch.nn
from RL.learning.DataSampler import DataSampler
from RL.Model.LinearValue import LinearValue
from RL.Model.SingleLayerValue import SingleLayerValue
from Playground.compare_policies import compare_policies
from Policy.ModelBasedPolicy import ModelBasedPolicy
from MiniMaxPolicy.MiniMaxPolicy import MiniMaxPolicy
from MiniMaxPolicy.Evaluator.SimpleEvaluators import ColoredCellsCountEvaluator
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from RL.Feature.KernelFeatures import KernelFeatureExtractor


class Trainer:

    def __init__(self, model, data_sampler, save_path='data/model.pt', self_play_batch_size=500,
                 train_epoch_count=800, minibatch_size=64, test_percentage=0.2, gamma=0.95, learning_rate=0.1):
        self.model = model
        self.data_sampler: DataSampler = data_sampler
        self.save_path = save_path

        self.self_play_batch_size = self_play_batch_size
        self.train_epoch_count = train_epoch_count
        self.minibatch_size = minibatch_size
        self.learning_rate = learning_rate
        self.test_percentage = test_percentage
        self.gamma = gamma

    def training_loop(self):

        data = self.data_sampler.sample_data_by_self_play_with_model(self.model, self.self_play_batch_size)
        torch.save(data, 'data/selfplay.pt')

        self.train_on_data(data, self.train_epoch_count)
        torch.save(model.state_dict(), self.save_path)
        self.evaluate_model(data)

    def train_on_data(self, data, epoch_count, print_every=50):
        train_features, train_game_values, test_features, test_game_values = self.split_data(data)
        optimizer = torch.optim.SGD(model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.MSELoss()

        for epoch in range(epoch_count):
            for i in range(0, train_features.shape[0] // self.minibatch_size):
                batch_features = train_features[i * self.minibatch_size: (i + 1) * self.minibatch_size, :]
                batch_values = train_game_values[i * self.minibatch_size: (i + 1) * self.minibatch_size]
                pred_game_values = self.model.forward(batch_features)
                pred_game_values = pred_game_values.squeeze(1)

                # Compute and print loss
                loss = criterion(pred_game_values, batch_values)

                # Zero gradients, perform a backward pass,
                # and update the weights.
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % print_every == 0:
                with torch.no_grad():
                    pred_game_values = model(test_features)
                    pred_game_values = pred_game_values.squeeze(1)
                    test_loss = criterion(pred_game_values, test_game_values)
                print('epoch {}, loss {:.5}, test loss: {:.5}'.format(epoch + 1, loss, test_loss))

    def split_data(self, data):
        features = data[:, : self.model.input_size]
        # -1 == winner
        # -2 == moves till end
        # -3 == next state value

        # Important place, we chose what to optimise here

        game_values = self.get_target_from_data(data)

        # features, predicted_value, moves_till_end, game_result
        train_n = int(data.shape[0] * (1 - self.test_percentage))

        train_features = features[:train_n]
        test_features = features[train_n:]
        train_game_values = game_values[:train_n]
        test_game_values = game_values[train_n:]

        return train_features, train_game_values, test_features, test_game_values

    def get_target_from_data(self, data):
        return data[:, -1] * (self.gamma ** data[:, -2])

    def evaluate_model(self, data):
        h, w = self.model.field_h, model.field_w
        model_policy = ModelBasedPolicy(model, h, w, 0.1)
        compare_to = MiniMaxPolicy(ColoredCellsCountEvaluator(), 1)
        compare_policies(model_policy, compare_to, 50, h, w)
        target = self.get_target_from_data(data)
        default_prediction_loss = ((abs(target - target.mean())).mean() ** 2)
        weights = torch.tensor([i for x in list(model.linear.weight) for i in x])

        print('max/mean/min/std weight: {:.3}/{:.3}/{:.3}/{:.3}'.format(weights.max(), weights.mean(), weights.min(),weights.std()))
        print('mse loss on mean over batch prediction  = {:.3}'.format(default_prediction_loss))


if __name__ == '__main__':
    feature_extractor = KernelFeatureExtractor()
    data_sampler = DataSampler(feature_extractor)
    model = SingleLayerValue(5, 5, 100)

    # model = SingleLayerValue(5, 5, 50)

    # model.load_state_dict(torch.load('data/linear4.pt'))
    # model.eval()

    trainer = Trainer(model, data_sampler, 'data/model5.pt', self_play_batch_size=10, minibatch_size=5,
                      train_epoch_count=50)
    data = torch.load('data/selfplay_AC2_20000_games.pt')
    data = data.float()

    for i in range(5):
        trainer.train_on_data(data, 1, print_every=1)
        trainer.evaluate_model(data)
