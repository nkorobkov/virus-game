# %%

import torch
import torch.nn

from RL.Model.ConvolutionValue import ConvolutionValue
from RL.learning.DataSampler import DataSampler
from Playground.compare_policies import compare_policies
from Policy.ModelBasedPolicy import ModelBasedPolicy
from MiniMaxPolicy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from MiniMaxPolicy.Evaluator.SimpleEvaluators import ActiveCountEvaluator
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from Playground.util import readable_time_since
from time import time


class Trainer:

    def __init__(self, model, data_sampler, save_path='data/model.pt', self_play_batch_size=500,
                 train_epoch_count=800, minibatch_size=64, test_percentage=0.2, gamma=0.9, learning_rate=0.001):
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

        features, labels = self.data_sampler.sample_data_by_self_play_with_model(self.model, self.self_play_batch_size)
        torch.save(features, 'data/selfplay-f.pt')
        torch.save(labels, 'data/selfplay-l.pt')

        self.train_on_data(features, labels, self.train_epoch_count)
        torch.save(self.model.state_dict(), self.save_path)
        self.evaluate_model(labels)

    def train_on_data(self, features, labels, epoch_count, print_every=50, eval_every=200):

        train_features, train_game_values, test_features, test_game_values = self.split_data(features, labels)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.MSELoss()
        t = time()
        for epoch in range(epoch_count):
            self.model.train(True)
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
                self.model.train(False)
                with torch.no_grad():
                    pred_game_values = self.model.forward(test_features)
                    pred_game_values = pred_game_values.squeeze(1)
                    test_loss = criterion(pred_game_values, test_game_values)
                print('epoch {}, loss {:.5}, test loss: {:.5}, time elapsed: {}'.format(epoch + 1, loss, test_loss,
                                                                                        readable_time_since(t)))
            if (epoch + 1) % eval_every == 0:
                self.evaluate_model(labels)
                torch.save(self.model.state_dict(), self.save_path.format(epoch))

    def split_data(self, features, labels):

        # -1 == winner
        # -2 == moves till end
        # -3 == next state value

        # Important place, we chose what to optimise here

        game_values = self.get_target_from_labels(labels)

        # features, predicted_value, moves_till_end, game_result
        train_n = int(features.shape[0] * (1 - self.test_percentage))

        train_features = features[:train_n]
        test_features = features[train_n:]
        train_game_values = game_values[:train_n]
        test_game_values = game_values[train_n:]

        return train_features, train_game_values, test_features, test_game_values

    def get_target_from_labels(self, labels):

        return labels[:, -1] * (self.gamma ** labels[:, -2])

    def evaluate_model(self, labels):
        self.model.train(False)
        h, w = self.model.field_h, self.model.field_w
        model_policy = ModelBasedPolicy(self.model, self.data_sampler.feature_extractor, h, w, exploration=0.05)

        model_new_6_epoch = ConvolutionValue(h, w)
        model_new_6_epoch.load_state_dict(torch.load('data/model8-conv-disc2-10iz10.pt'))
        model_new_6_epoch.eval()
        model_6 = ModelBasedPolicy(model_new_6_epoch, PlainFeatureExtractor(), h, w, 0.05)
        compare_to = model_6

        compare_policies(model_policy, compare_to, 8, h, w)
        target = self.get_target_from_labels(labels)
        self.print_linear_weights_stat()

        default_prediction_loss = ((abs(target - target.mean())).mean() ** 2)
        print('mse loss on mean over batch prediction  = {:.3}'.format(default_prediction_loss))

    def print_linear_weights_stat(self):
        ln = 1
        for m in self.model.modules():
            if isinstance(m, torch.nn.Linear):
                print('Linear Layer {}, in: {}, out: {} max/mean/min/std weight: {:.3}/{:.3}/{:.3}/{:.3}'.format(
                    ln, m.in_features, m.out_features, m.weight.max(), m.weight.mean(), m.weight.min(), m.weight.std()))
                ln += 1


if __name__ == '__main__':
    feature_extractor = PlainFeatureExtractor()
    data_sampler = DataSampler(feature_extractor)
    model = ConvolutionValue(8, 8)

    #model.load_state_dict(torch.load('data/model8-conv-disc2.pt'))
    # model.eval()

    features = torch.load('data/selfplay_AC2_88_games-plain-features-u.pt').float()
    labels = torch.load('data/selfplay_AC2_88_games-plain-labels-u.pt').float()
    print(features.shape)
    trainer = Trainer(model, data_sampler, save_path='data/model8-conv-disc-{}-ep-95.pt', minibatch_size=64, gamma=0.95)

    trainer.train_on_data(features, labels, 15, 1, 1)

    torch.save(trainer.model.state_dict(), trainer.save_path)
