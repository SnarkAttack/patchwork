import logging
import numpy as np
import random
from patchwork.patch import PATCH1
from patchwork.game_state import PatchworkGameState
from patchwork.constants import PLAYER1, PLAYER2
from ai.base_net import PatchworkBaseNet
from ai.tree import MLTree

def play_game(model):
    # Initialize new game state
    state = PatchworkGameState()

    tree = MLTree(model, state)

    while not state.is_terminal():
        
        # state.display_game_state()

        best_action = tree.select_best_action_time(2000, maximal=True)

        print(f"Iterations run: {tree.num_iterations_run}\n")
        print(f"Action to take: {best_action}")

        state = state.take_action(best_action)

        tree = MLTree(model, state)

    state.display_game_state()
    print(state.get_reward())


if __name__ == "__main__":

    logger = logging.getLogger("patchwork")
    logger.setLevel(logging.WARNING)

    random.seed(0)

    net = PatchworkBaseNet()

    play_game(net)



