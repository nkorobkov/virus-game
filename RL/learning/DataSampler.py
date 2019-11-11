import time
import torch
import torch.nn
import numpy.random
from Game.GameState import GameState
from RL.Feature.PlainFearutesExtractor import PlainFeatureExtractor
from Policy.exceptions import NoValidMovesException
from Game.Teams import Teams
from Policy.Policy import EstimatingPolicy
from RL.Feature.FeatureExtractor import FeatureExtractor
from MiniMaxPolicy.ExplorativeMiniMaxPolicy import ExplorativeMiniMaxPolicy
from MiniMaxPolicy.Evaluator.SimpleEvaluators import ColoredCellsCountEvaluator
from random import choice

from Playground.util import readable_time_since
from typing import Tuple


class DataSampler:

    def __init__(self, feature_extractor: FeatureExtractor, exploration_rate=0.1, win_value=1):
        self.exploration_rate = exploration_rate
        self.win_value_tensor = torch.tensor([win_value], requires_grad=False).float()
        self.feature_extractor = feature_extractor

    def sample_data_by_self_play_with_policy(self, policy: EstimatingPolicy, n=100, h=5, w=5,
                                             augment=True, randomize=False, print_every=50):
        t = time.time()
        print('playing {} selfplay games ...'.format(n))
        game_states, move_counts, winners = [], [], []
        for i in range(n):
            game_ss, mc, ws = self.sample_data_from_single_game_with_policy(policy, h, w, randomize=randomize)
            game_states.extend(game_ss)
            move_counts.extend(mc)
            winners.extend(ws)
            if (i + 1) % print_every == 0:
                print('{}/{} games sampled in {}'.format(i + 1, n, readable_time_since(t)))

        if augment:
            game_states.extend([DataSampler.mirror_game_state_norm(x) for x in game_states])
            move_counts.extend(move_counts)
            winners.extend(winners)

        features = self.feature_extractor.get_features(game_states)
        move_counts = torch.tensor(move_counts, dtype=torch.int8)
        move_counts.unsqueeze_(1)
        winners = torch.tensor(winners, dtype=torch.int8)
        winners.unsqueeze_(1)
        labels = torch.cat((move_counts, winners), dim=1)
        print('sampled data from {} moves'.format(len(game_states)))
        return features, labels

    @staticmethod
    def mirror_game_state_norm(game_state: GameState):
        new_field = [0] * len(game_state.field)
        w = game_state.size_w
        h = game_state.size_h
        for i in range(h):
            for j in range(w):
                new_field[h * j + i] = game_state.field[h * i + j]
        return GameState.from_field_list(h,
                                         w,
                                         new_field,
                                         game_state.to_move)

    def sample_data_from_single_game_with_policy(self, policy, h, w, randomize=False):
        data = []
        game = GameState(h, w)
        move_count = 0

        while True:

            try:
                if move_count < 2 and randomize:
                    game.make_move(choice(list(game.get_all_moves())))
                else:
                    move = policy.get_move(game)
                    game.make_move(move)
                data.append(GameState.copy(game))
                move_count += 1

            except NoValidMovesException as e:
                winner = Teams.other(e.for_team)
                move_counts = list(range(move_count - 1, -1, -1))

                # after feature extraction all
                # fields will be like it is blue moving, so switch winner for red moving fields
                winners = [(-1 if i % 2 == 0 else 1) * winner for i in range(move_count)]
                return data, move_counts, winners

    def sample_data_by_self_play_with_model(self, model: torch.nn.Module, n=100):
        t = time.time()

        print('playing {} selfplay games ...'.format(n))
        # pool = Pool(4)
        # #data = pool.map(self.sample_data_from_single_game, [model] * n)
        # data = [item for sublist in data for item in sublist]
        data = []
        winners = []
        move_counts = []
        for i in range(n):
            play_data, play_move_counts, play_winners = self.sample_data_from_single_game_with_model(model)
            data.extend(play_data)
            winners.extend(play_winners)
            move_counts.extend(play_move_counts)
            if (i + 1) % 10 == 0:
                print('{}/{} games sampled in {}'.format(i + 1, n, readable_time_since(t)))
        print('sampled data from {} moves'.format(len(data)))
        move_counts = torch.tensor(move_counts, dtype=torch.int8)
        move_counts.unsqueeze_(1)
        winners = torch.tensor(winners, dtype=torch.int8)
        winners.unsqueeze_(1)
        labels = torch.cat((move_counts, winners), dim=1)

        return torch.stack(data, dim=0), labels

    def sample_data_from_single_game_with_model(self, model: torch.nn.Module):
        data = []
        game = GameState(model.field_h, model.field_w)
        move_count = 0
        move_counts = []
        while True:
            try:
                step_data, game = self.sample_data_from_step_with_model(game, model)
                move_counts.append(move_counts)
                data.append(step_data)
                move_count += 1
            except NoValidMovesException as e:
                winner = Teams.other(e.for_team)
                last_state_game_features = self.feature_extractor.get_features([game])
                last_state_game_features.squeeze_(0)
                data.append(last_state_game_features)
                move_counts.append(move_counts)
                data = torch.stack(data, dim=0)
                move_counts = [(i - move_count) * -1 for i in move_counts]

                winners = [(-1 if i % 2 == 0 else 1) * winner for i in range(move_count)]
                return data, move_counts, winners

    def sample_data_from_step_with_model(self, game, model) -> Tuple[torch.Tensor, GameState]:
        moves = list(game.get_all_moves())
        next_states = [game.get_copy_with_move(move) for move in moves]
        if not next_states:
            raise NoValidMovesException(game.to_move, 'No move for {}'.format(game.to_move))
        with torch.no_grad():
            features_for_all_states = self.feature_extractor.get_features([game] + next_states).float()
            v: torch.Tensor = model.forward(features_for_all_states[1:])

        best_move_value, best_move_index = v.min(0)
        next_state = next_states[int(best_move_index)]

        if numpy.random.random() < self.exploration_rate:
            next_state = numpy.random.choice(next_states)
        return features_for_all_states[0], next_state


if __name__ == '__main__':
    ds = DataSampler(feature_extractor=PlainFeatureExtractor())

    evaluator = ColoredCellsCountEvaluator()

    policy = ExplorativeMiniMaxPolicy(evaluator, exploration_rate=0.08, depth=2)

    features, labels = ds.sample_data_by_self_play_with_policy(policy, n=2000, h=8, w=8, augment=True, randomize=True,
                                                               print_every=5)

    torch.save(features, 'data/selfplay_AC2_88_games-plain-features3.pt')
    torch.save(labels, 'data/selfplay_AC2_88_games-plain-labels3.pt')
    # h, w = 5, 5
    # model = ConvolutionValue(h, w)
    # model.load_state_dict(torch.load('data/model5-conv-disc.pt'))
    # model.eval()
