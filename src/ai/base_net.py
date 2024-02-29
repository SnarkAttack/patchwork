import torch
import torch.nn as nn
from patchwork.game_state import PatchworkGameState

class PatchworkBaseNet(torch.nn.Module):

    def __init__(self):
        super().__init__()

        self._board_conv_1 = nn.Conv2d(2, 4, (5, 5))
        self._board_conv_2 = nn.Conv2d(4, 8, (3, 3))
        self._board_dropout = nn.Dropout(p=.2)
        self._board_relu = nn.ReLU()

        self._player_linear_1 = nn.Linear(39, 100)
        self._player_linear_2 = nn.Linear(100, 40)
        self._player_linear_3 = nn.Linear(40, 18)
        self._player_dropout = nn.Dropout(p=.2)
        self._player_relu = nn.ReLU()

        self._patch_conv_1 = nn.Conv2d(3, 4, (3, 3))
        self._patch_dropout = nn.Dropout(p=.2)
        self._patch_relu = nn.ReLU()

        self._output_conv_1 = nn.Conv2d(16, 64, (2, 2))
        self._output_conv_2 = nn.Conv2d(64, 64, (2, 2))
        self._output_relu = nn.ReLU()

        self._value_linear_1 = nn.Linear(64, 16)
        self._value_linear_2 = nn.Linear(16, 1)

        self._policy_linear_1 = nn.Linear(64, 128)
        # Output policy is any of the first 3 tiles plus a special tile
        # in any of the 81 board location, plus advancing the token
        all_action_count = 3*9*9*4 + 1*9*9 + 1
        self._policy_linear_2 = nn.Linear(128, all_action_count)
        self._policy_softmax = nn.Softmax()

    def forward(self, game_state: PatchworkGameState):

        boards, players, patches = game_state.convert_to_network_inputs()

        board_out = self._board_conv_1(boards)
        board_out = self._board_conv_2(board_out)
        board_out = self._board_dropout(board_out)
        board_out = self._board_relu(board_out)

        player_out = self._player_linear_1(players)
        player_out = self._player_linear_2(player_out)
        player_out = self._player_linear_3(player_out)
        player_out = self._player_dropout(player_out)
        player_out = self._player_relu(player_out)
        player_out = torch.reshape(player_out, (-1, 3, 3))

        patch_out = self._patch_conv_1(patches)
        patch_out = self._patch_dropout(patch_out)
        patch_out = self._patch_relu(patch_out)

        # print(board_out.shape)
        # print(player_out.shape)
        # print(patch_out.shape)

        output = torch.cat([board_out, player_out, patch_out], dim=0)
        output = self._output_conv_1(output)
        output = self._output_conv_2(output)
        output = self._output_relu(output)

        output = torch.flatten(output)

        value_out = self._value_linear_1(output)
        value_out = self._value_linear_2(value_out)

        policy_out = self._policy_linear_1(output)
        policy_out = self._policy_linear_2(policy_out)
        policy_out = self._policy_softmax(policy_out)

        return policy_out, value_out




