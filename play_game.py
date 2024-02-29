import logging
import numpy as np
import random
from patchwork.patch import PATCH1
from patchwork.game_state import PatchworkGameState
from patchwork.constants import PLAYER1, PLAYER2
from mcts.tree import BaseTree

if __name__ == "__main__":

    logger = logging.getLogger("patchwork")
    logger.setLevel(logging.WARNING)

    random.seed(0)

    # Initialize new game state
    state = PatchworkGameState()

    turn_count = 0

    tree = BaseTree(state)

    while not state.is_terminal():

        # state.display_game_state()

        if state.get_current_player == PLAYER1:
            maximize = True
        else:
            maximize = False

        best_action = tree.select_best_action_time(1000, maximal=maximize)

        print(f"Iterations run: {tree.num_iterations_run}\n")

        print(f"Action to take: {best_action}")

        state = state.take_action(best_action)

        tree = tree.create_tree_from_action(best_action)

        turn_count += 1

        # if turn_count >= 4:
        #     break

    state.display_game_state()

    