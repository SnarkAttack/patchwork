import logging
import numpy as np
from .patch import Patch
from .constants import RotationDirection

logger = logging.getLogger(__name__)

class QuiltBoard:

    def __init__(self, board_shape=(9, 9)):

        self._board = np.zeros(board_shape, dtype=np.int8)

    def visualize_board(self):
        print(self._board)

    def get_empty_indices(self):
        return np.argwhere(self._board == 0)
    
    def _shift_patch_indices(self, patch_indices, shift_idx):

        shifted_indices = np.array([patch_idx + shift_idx for patch_idx in patch_indices])

        return shifted_indices

    def is_patch_at_index_legal(self, patch: Patch, dir: RotationDirection, index):

        patch_indices = patch.get_used_indices(rotate_count=dir)

        shifted_indices = self._shift_patch_indices(patch_indices, index)

        for shift in shifted_indices:
            # Check if any part of patch is hanging over edge of board
            if shift[0] >= self._board.shape[0] or shift[1] >= self._board.shape[1]:
                return False
            # Check if any part of patch is overlapping another already on board
            if self._board[shift[0], shift[1]] != 0:
                return False

        return True
    
    def get_all_board_indices(self):
        board_indices = np.indices(self._board.shape)
        board_indices = np.transpose(np.reshape(board_indices, (2, -1)))
        return board_indices

    def find_legal_patch_locations(self, patch: Patch):
        
        board_indices = self.get_all_board_indices()

        legal_locations = []

        for dir in RotationDirection:

            mask = np.ones(len(board_indices), dtype=bool)

            for i, board_idx in enumerate(board_indices):

                mask[i] = self.is_patch_at_index_legal(patch, dir, board_idx)
            
            valid_indices = board_indices[mask]

            if len(valid_indices) > 0:
                legal_locations.append((valid_indices, dir))

        return legal_locations
    
    def add_patch_to_board(self, patch: Patch, dir: RotationDirection, idx):
        if not self.is_patch_at_index_legal(patch, dir, idx):
            logger.info('Trying to perform illegal move')
            return False
        
        patch_indices = patch.get_used_indices(rotate_count=dir.value)
        shifted_indices = self._shift_patch_indices(patch_indices, idx)
        
        self._board[shifted_indices[:,0], shifted_indices[:,1]] = patch.id

        return True
        
