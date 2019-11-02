import time
from time import strftime
from time import gmtime
import torch
import torch.nn
import numpy.random
from Game.GameState import GameState
from RL.Model.LinearValue import LinearValue
from RL.Feature.KernelFeatures import KernelFeatureExtractor
from Policy.exceptions import NoValidMovesException
from Game.Teams import Teams

from multiprocessing.pool import Pool

from typing import Tuple

self_play_batch_size = 100


def readable_time_since(t):
    return strftime("%M m. %S sec.", gmtime(int(time.time() - t)))


# features, predicted_value, moves_till_end, game_result
# exploration_rate = 0.1
# win_value_tensor = torch.tensor([100]).float()
# feature_extractor = KernelFeatureExtractor()


class DataCollector:

    def __init__(self, exploration_rate=0.1, win_value=100, feature_extractor=KernelFeatureExtractor()):
        self.exploration_rate = exploration_rate
        self.win_value_tensor = torch.tensor([win_value], requires_grad=False).float()
        self.feature_extractor = feature_extractor

    def collect_data_by_self_play(self, model: torch.nn.Module, n=self_play_batch_size):
        t = time.time()

        print('playing {} selfplay games ...'.format(n))
        # pool = Pool(4)
        # #data = pool.map(self.collect_data_from_single_game, [model] * n)
        # data = [item for sublist in data for item in sublist]
        data = []
        for i in range(n):
            data.extend(self.collect_data_from_single_game(model))
            if (i + 1) % 10 == 0:
                print('{}/{} games sampled in {}'.format(i + 1, n, readable_time_since(t)))
        return torch.stack(data, dim=0)

    def collect_data_from_single_game(self, model: torch.nn.Module):
        data = []
        game = GameState(model.field_h, model.field_w)
        move_count = 0
        while True:
            try:
                step_data, game = self.collect_data_from_step(game, model)
                data.append(torch.cat((step_data, torch.tensor([move_count], requires_grad=False).float())))
                move_count += 1
            except NoValidMovesException as e:
                winner = Teams.other(e.for_team)
                last_state_game_features = self.feature_extractor.get_features([game])
                last_state_game_features.squeeze_(0)
                # IDEA: change to store features as  int8 separately.
                data.append(torch.cat(
                    (last_state_game_features.float(), self.win_value_tensor * winner,
                     torch.tensor([move_count], requires_grad=False).float())))
                data = torch.stack(data, dim=0)
                data[:, -1] = (data[:, -1] - move_count) * -1
                data = torch.cat((data, torch.ones((data.shape[0], 1), requires_grad=False) * winner), dim=1)
                return data

    def collect_data_from_step(self, game, model) -> Tuple[torch.Tensor, GameState]:
        moves = list(game.get_all_moves())
        next_states = [game.get_copy_with_move(move) for move in moves]
        if not next_states:
            raise NoValidMovesException(game.to_move, 'No move for {}'.format(game.to_move))
        with torch.no_grad():
            features_for_all_states = self.feature_extractor.get_features([game] + next_states).float()
            v: torch.Tensor = model.forward(features_for_all_states[1:])

        if game.to_move == Teams.BLUE:
            best_move_value, best_move_index = v.max(0)
        else:
            best_move_value, best_move_index = v.min(0)
        next_state = next_states[int(best_move_index)]

        if numpy.random.random() < self.exploration_rate:
            next_state = numpy.random.choice(next_states)
        return torch.cat((features_for_all_states[0], best_move_value)), next_state

    def collect_endgame_states_from_random_games(self, h, w, n=self_play_batch_size):
        data = []
        for i in range(n):
            t = time.time()
            game = GameState(h, w)
            if not i % 500:
                print('game {}/{} in {} sec.'.format(i + 1, n, readable_time_since(t)
                                                     ))
            while True:

                moves = list(game.get_all_moves())
                if moves:
                    i = numpy.random.randint(0, len(moves))
                    game.make_move(moves[i])
                else:
                    winner = Teams.other(game.to_move)
                    features = self.feature_extractor.get_features([game])
                    features = features.squeeze(0)

                    # we do not show to_move value, since it is strongly correlaged with winner
                    features[0] = 0

                    data.append(torch.cat(
                        (features.float(),
                         self.win_value_tensor * winner,
                         torch.tensor([0], requires_grad=False).float(),
                         torch.tensor([winner], requires_grad=False).float()),
                        dim=0))
                    break
        return torch.stack(data, dim=0)

