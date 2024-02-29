import random
import numpy as np

class Patch:

    def __init__(self,
                 id,
                 layout,
                 num_buttons,
                 button_cost,
                 time_cost):

        self._id = id
        self._layout = layout
        self._num_buttons = num_buttons
        self._button_cost = button_cost
        self._time_cost = time_cost

    def __str__(self):
        return f"{self._id}"

    @property
    def id(self):
        return self._id

    @property
    def layout(self):
        return self._layout
    
    @property
    def num_buttons(self):
        return self._num_buttons
    
    @property
    def button_cost(self):
        return self._button_cost
    
    @property
    def time_cost(self):
        return self._time_cost

    def get_used_indices(self, rotate_count=0):
        rotated_layout = np.rot90(self._layout, k=rotate_count)
        return np.argwhere(rotated_layout == 1)


PATCH1 = Patch(1,
               np.array([[1, 0],
                         [1, 1]]),
               0, 1, 3)

PATCH2 = Patch(2,
               np.array([[0,1,0],
                         [1,1,1],
                         [0,1,0]]),
               2, 5, 4)

PATCH3 = Patch(3,
               np.array([[0,1,0],
                         [0,1,1],
                         [1,1,0],
                         [0,1,0]]),
               0, 2, 1)

# TODO: Double check size of this one
PATCH4 = Patch(4,
               np.array([[1,1,1,1,1]]),
               1, 7, 1)

PATCH5 = Patch(5,
               np.array([[0,1,1],
                         [0,1,1],
                         [1,1,0]]),
                3, 8, 6)

PATCH6 = Patch(6,
               np.array([[0, 1],
                         [1, 1]]),
                0, 3, 1)

PATCH7 = Patch(7,
               np.array([[0, 0, 0, 1],
                         [1, 1, 1, 1],
                         [1, 0, 0, 0]]),
                0, 1, 2)

PATCH8 = Patch(8,
               np.array([[0, 1],
                         [1, 1],
                         [0, 1]]),
                0, 2, 2)

PATCH9 = Patch(9,
               np.array([[1, 0],
                         [1, 1],
                         [1, 1]]),
                0, 2, 2)

PATCH10 = Patch(10,
                np.array([[0, 1],
                          [1, 1],
                          [1, 1],
                          [1, 0]]),
                0, 4, 2)

PATCH11 = Patch(11,
                np.array([[0, 0, 1],
                          [0, 1, 1],
                          [1, 1, 0]]),
                3, 10, 4)

PATCH12 = Patch(12,
                np.array([[0, 1, 1, 0],
                          [1, 1, 1, 1]]),
                2, 7, 4)

PATCH13 = Patch(13,
                np.array([[0, 1, 1, 1],
                          [1, 1, 0, 0]]),
                1, 2, 3)

PATCH14 = Patch(14,
                np.array([[1, 1, 1, 1],
                          [1, 1, 0, 0]]),
                3, 10, 5)

PATCH15 = Patch(15,
                np.array([[1, 1],
                          [1, 1]]),
                2, 6, 5)

PATCH16 = Patch(16,
                np.array([[0, 1, 0, 0],
                          [1, 1, 1, 1],
                          [0, 1, 0, 0]]),
                1, 0, 3)

PATCH17 = Patch(17,
                np.array([[1, 0, 1],
                          [1, 1, 1],
                          [1, 0, 1]]),
                0, 2, 3)

PATCH18 = Patch(18,
                np.array([[1, 0, 0, 1],
                          [1, 1, 1, 1]]),
                1, 1, 5)

PATCH19 = Patch(19,
                np.array([[0, 1],
                          [1, 1],
                          [1, 0]]),
                3, 7, 6)

PATCH20 = Patch(20,
                np.array([[0, 1],
                          [0, 1],
                          [1, 1],
                          [0, 1]]),
                1, 3, 4)

PATCH21 = Patch(21,
                np.array([[1, 1, 1, 1]]),
                1, 3, 3)

PATCH22 = Patch(22,
                np.array([[0, 1, 0],
                          [0, 1, 0],
                          [0, 1, 0],
                          [1, 1, 1]]),
                2, 7, 2)

PATCH23 = Patch(23,
                np.array([[0, 1],
                          [1, 1],
                          [1, 0]]),
                1, 3, 2)

PATCH24 = Patch(24,
                np.array([[0, 1],
                          [0, 1],
                          [1, 1]]),
                2, 4, 6)

PATCH25 = Patch(25,
                np.array([[0, 1],
                          [0, 1],
                          [0, 1],
                          [1, 1]]),
                2, 10, 3)

PATCH26 = Patch(26,
                np.array([[0, 1, 1, 0],
                          [1, 1, 1, 1],
                          [0, 1, 1, 0]]),
                1, 5, 3)

PATCH27 = Patch(27,
                np.array([[0, 0, 1, 0, 0],
                          [1, 1, 1, 1, 1],
                          [0, 0, 1, 0, 0]]),
                1, 1, 4)

PATCH28 = Patch(28,
                np.array([[0, 1, 0],
                          [1, 1, 1],
                          [1, 0, 1]]),
                2, 3, 6)

PATCH29 = Patch(29,
                np.array([[1, 0, 1],
                          [1, 1, 1]]),
                    0, 1, 2)

PATCH30 = Patch(30,
                np.array([[1, 1, 1]]),
                0, 2, 2)

PATCH31 = Patch(31,
                np.array([[0, 0, 1],
                          [1, 1, 1]]),
                1, 4, 2)

PATCH32 = Patch(32,
                np.array([[0, 1, 0],
                          [0, 1, 0],
                          [1, 1, 1]]),
                2, 5, 5)

PATCH33 = Patch(33,
                np.array([[1, 1]]),
                0, 2, 1)

PATCH_S = Patch(-1,
                np.array([[1]]),
                0, 0, 0)


def generate_patch_setup():

    patch_list = [
        PATCH1,
        PATCH2,
        PATCH3,
        PATCH4,
        PATCH5,
        PATCH6,
        PATCH7,
        PATCH8,
        PATCH9,
        PATCH10,
        PATCH11,
        PATCH12,
        PATCH13,
        PATCH14,
        PATCH15,
        PATCH16,
        PATCH17,
        PATCH18,
        PATCH19,
        PATCH20,
        PATCH21,
        PATCH22,
        PATCH23,
        PATCH24,
        PATCH25,
        PATCH26,
        PATCH27,
        PATCH28,
        PATCH29,
        PATCH30,
        PATCH31,
        PATCH32
    ]

    random.shuffle(patch_list)

    patch_list.append(PATCH33)

    return patch_list

