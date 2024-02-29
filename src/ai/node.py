from mcts.node import BaseNode
from patchwork.game_state import PatchworkGameState
import math

class MLNode(BaseNode):

    def __init__(self, state: PatchworkGameState, parent, probability):
        super().__init__(state, parent)

        self._child_probs = []
        self._probability = probability

    @property
    def child_probs(self):
        return self._child_probs
    
    @child_probs.setter
    def child_probs(self, c):
        self._child_probs = c

    def expand(self, model):

        all_actions = self._state.get_all_actions()

        policy_out, value_out = model(self._state)
        self._child_probs = policy_out
        self._total_value = value_out

        for i, action in enumerate(all_actions):
            new_state = self._state.take_action(action)
            new_child = MLNode(new_state, parent=self, probability=self._child_probs[i])
            self.children[action] = new_child

        return self.select_best_child(C=math.sqrt(2))