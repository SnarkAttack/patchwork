import numpy as np

from patchwork.quilt_board import QuiltBoard
from patchwork.patch import PATCH1
from patchwork.constants import RotationDirection

def test_empty_quilt_board():

    qb = QuiltBoard()

    assert len(qb.get_empty_indices()) == 81

def test_add_patch():

    qb = QuiltBoard((3, 3))

    assert qb.is_patch_at_index_legal(PATCH1, RotationDirection.UP, np.array([0, 0])) == True

    qb.add_patch_to_board(PATCH1, RotationDirection.UP, np.array([0, 0]))

    assert qb.is_patch_at_index_legal(PATCH1, RotationDirection.UP, np.array([0, 0])) == False
