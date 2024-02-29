import logging
import torch
import numpy as np
from mcts.state import BaseState
from copy import deepcopy

from .constants import PLAYER1, PLAYER2, RotationDirection
from .patch import generate_patch_setup, PATCH_S
from .quilt_board import QuiltBoard
from .time_board import TimeBoard
from .action import PatchworkAction, PlacePatchAction, AdvanceTokenAction, PlaceSpecialPatchAction

logger = logging.getLogger(__name__)

class PatchworkGameState(BaseState):

    def __init__(self):

        self._players = {
            PLAYER1: 'Player 1',
            PLAYER2: 'Player 2'
        }

        self._buttons = {
            PLAYER1: 5,
            PLAYER2: 5
        }

        # Only holds 7 bonus points for finishing 7x7 grid
        self._bonus_points = {
            PLAYER1: 0,
            PLAYER2: 0
        }

        self._special_patch_count = {
            PLAYER1: 0,
            PLAYER2: 0
        }
        
        self._token_location = 0

        self._patches = generate_patch_setup()

        self._player_boards = {
            PLAYER1: QuiltBoard(),
            PLAYER2: QuiltBoard()
        }

        self._num_patches = 33

        self._patches_owned = {
            PLAYER1: [],
            PLAYER2: []
        }

        self._time_board = TimeBoard()

        self._current_player = PLAYER1

    def is_player_done(self, player_id):
        return self._time_board.is_player_done(player_id)
    
    def get_player_score(self, player_id):
        return self._buttons[player_id] + self._bonus_points[player_id] - 2*len(self._player_boards[player_id].get_empty_indices())
    
    def get_player_income(self, player_id):
        income = sum([patch.num_buttons for patch in self._patches_owned[player_id]])
        logger.debug(f"{self._players[player_id]} get income of {income}")
        return income
    
    def visualize_player_board(self, player_id):
        self._player_boards[player_id].visualize_board()
    
    def set_next_player(self):
        if self._special_patch_count[PLAYER1] > 0:
            self._current_player = PLAYER1
        elif self._special_patch_count[PLAYER2] > 0:
            self._current_player = PLAYER2
        self._current_player = self._time_board.determine_next_player()

    def get_current_player(self):
        return self._current_player
    
    def _get_next_patches(self, num_patches=3):
        indices = [(self._token_location+i)%len(self._patches) for i in range(num_patches)]
        valid_patches = [self._patches[i] for i in indices]
        return valid_patches

    def get_possible_actions(self):
        possible_actions = []

        if self._special_patch_count[self._current_player] > 0:
            valid_locations = self._player_boards[self._current_player].find_legal_patch_locations(PATCH_S)
            indices = valid_locations[0][0]
            for board_index in indices:
                possible_actions.append(PlaceSpecialPatchAction(self._current_player, board_index))
        else:

            for patch_idx, patch in enumerate(self._get_next_patches()):

                if self._buttons[self._current_player] >= patch.button_cost:

                    valid_locations = self._player_boards[self._current_player].find_legal_patch_locations(patch)

                    for indices, direction in valid_locations:
                        for board_index in indices:
                            possible_actions.append(PlacePatchAction(self._current_player, patch, patch_idx, direction, board_index))

            possible_actions.append(AdvanceTokenAction(self._current_player))

        return possible_actions
    
    def get_all_actions(self):

        all_actions = []

        board_indices = self._player_boards[self._current_player].get_all_board_indices()

        for patch_idx, patch in enumerate(self._get_next_patches()):
            for board_index in board_indices:
                for direction in RotationDirection:
                    all_actions.append(PlacePatchAction(self._current_player, patch, patch_idx, direction, board_index))

        for board_index in board_indices:
            all_actions.append(PlaceSpecialPatchAction(self._current_player, board_index))

        all_actions.append(AdvanceTokenAction(self._current_player))

        return all_actions

                                            
    def take_action(self, action: PatchworkAction) -> BaseState:
        
        next_state = deepcopy(self)
        player_id = action.player_id

        if isinstance(action, PlaceSpecialPatchAction):
            patch_added = next_state._player_boards[player_id].add_patch_to_board(action.patch, action.dir, action.index)
            if patch_added:
                next_state._patches_owned[player_id].append(action.patch)
            next_state._special_patch_count[player_id] -= 1
        elif isinstance(action, PlacePatchAction):
            patch_added = next_state._player_boards[player_id].add_patch_to_board(action.patch, action.dir, action.index)
            if patch_added:
                next_state._patches_owned[player_id].append(action.patch)
            next_state._buttons[player_id] -= action.patch.button_cost
            income_triggers, special_patches = next_state._time_board.move_player_forward(action.player_id, action.patch.time_cost)
            next_state._buttons[player_id] += next_state.get_player_income(player_id) * income_triggers
            next_state._special_patch_count[player_id] += special_patches
            next_state._token_location = (next_state._token_location + [patch.id for patch in next_state._get_next_patches()].index(action.patch.id)) % len(next_state._patches)
            next_state._patches.pop(next_state._token_location)
        elif isinstance(action, AdvanceTokenAction):
            spaces_to_advance = next_state._time_board.determine_spaces_to_advance(player_id)
            next_state._buttons[player_id] += spaces_to_advance
            income_triggers, special_patches = next_state._time_board.move_player_forward(player_id, spaces_to_advance)
            next_state._buttons[player_id] += next_state._buttons[player_id] * income_triggers
            next_state._special_patch_count[player_id] += special_patches
        else:
            raise NotImplementedError("Unknown Action Type")
        
        next_state.set_next_player()
        self._get_next_patches()

        return next_state
    
    def is_terminal(self) -> bool:
        return (self.is_player_done(PLAYER1) and self.is_player_done(PLAYER2)) or len(self._patches) == 0
    
    def get_reward(self) -> float:
        return self.get_player_score(PLAYER1) - self.get_player_score(PLAYER2)
    
    def display_player_stats(self, player_id):
        print(
            f"{self._players[player_id]}:\n\t" + 
            f"Score: {self.get_player_score(player_id)}\n\t" + 
            f"Buttons: {self._buttons[player_id]}\n\t" + 
            f"Location: {self._time_board._locations[player_id]}"
        )
        self.visualize_player_board(player_id)
        print()
    
    def display_game_state(self):

        logger.debug("TEST")

        self.display_player_stats(PLAYER1)
        self.display_player_stats(PLAYER2)

        print(f"Patches: {[self._patches[(self._token_location+i)%len(self._patches)].id for i in range(len(self._patches))]} ({len(self._patches)})")

    def convert_player_to_array(self, player_id):

        # Array is [buttons, points, special_patches, player location, patches_owned (one hot encoded), token_location]
        one_hot_patches_owned = np.zeros((self._num_patches,))
        one_hot_patches_owned[[patch.id for patch in self._patches_owned[player_id]]] = 1

        player_stats = np.array([
            self._buttons[player_id],
            self.get_player_score(player_id),
            self._special_patch_count[player_id],
            self._time_board._locations[player_id]
        ] + list(one_hot_patches_owned) + [self._current_player, self._token_location], dtype=np.int32)

        return player_stats

    def convert_board_to_occupied_only(self, player_id):

        board = deepcopy(self._player_boards[player_id]._board)
        board[board != 0] = 1

        return board
    
    def stack_next_patches(self):   
        next_patches = self._get_next_patches()

        max_shape = (5, 5)

        patch_stack = np.zeros((len(next_patches), max_shape[0], max_shape[1]))

        for i, patch in enumerate(next_patches):
            padded_patch = np.pad(patch._layout, [(0, max_shape[0]-patch._layout.shape[0]), (0, max_shape[1]-patch._layout.shape[1])], mode='constant')
            patch_stack[i] += padded_patch

        return patch_stack

    def convert_to_network_inputs(self):

        boards = np.stack([self.convert_board_to_occupied_only(PLAYER1), self.convert_board_to_occupied_only(PLAYER2)])
        players = np.stack([self.convert_player_to_array(PLAYER1), self.convert_player_to_array(PLAYER2)])
        patches = self.stack_next_patches()

        return torch.from_numpy(boards).type(torch.FloatTensor), torch.from_numpy(players).type(torch.FloatTensor), torch.from_numpy(patches).type(torch.FloatTensor)
