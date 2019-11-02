# %%

import torch
import torch.nn
from RL.learning.data_collection import DataCollector
from RL.Model.LinearValue import LinearValue


def training_loop(model, iteration=0):
    data_collector = DataCollector()

    data = data_collector.collect_data_by_self_play(model, 150)
    torch.save(data, 'data/selfplay.pt')

    train_on_data(model, data, iteration)
    torch.save(model.state_dict(), 'data/linear.pt')


def train_on_data(model, data, iteration=0, epoch_count=400):
    train_features, train_game_values, test_features, test_game_values = split_data(data)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    criterion = torch.nn.MSELoss()

    for epoch in range(epoch_count):

        pred_game_values = model(train_features)
        pred_game_values = pred_game_values.squeeze(1)

        # Compute and print loss
        loss = criterion(pred_game_values, train_game_values)
        # Zero gradients, perform a backward pass,
        # and update the weights.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 50 == 0:
            with torch.no_grad():
                pred_game_values = model(test_features)
                pred_game_values = pred_game_values.squeeze(1)
                test_loss = criterion(pred_game_values, test_game_values)
            print('it: {} epoch {}, loss {:.5}, test loss: {:.5}'.format(iteration, epoch + 1, loss, test_loss))


# %%

def split_data(data):
    features = data[:, : model.input_size]
    game_values = data[:, model.input_size]

    # features, predicted_value, moves_till_end, game_result
    train_n = int(data.shape[0] * 0.8)
    train_features = features[:train_n]
    test_features = features[train_n:]
    train_game_values = game_values[:train_n]
    test_game_values = game_values[train_n:]

    return train_features, train_game_values, test_features, test_game_values


if __name__ == '__main__':

    model = LinearValue(8, 8)
    model.load_state_dict(torch.load('data/linear.pt'))
    model.eval()

    # data = torch
    # train_on_data(model, torch.load('data/random_endgames.pt'), epoch_count=4000)
    # torch.save(model.state_dict(), 'data/linear.pt')

    for i in range(40):
        training_loop(model, i)
