from mcts.tree import BaseTree
from ai.node import MLNode
import math


class MLTree(BaseTree):

    def __init__(self, model, game_state, C=math.sqrt(2)):
        super().__init__(game_state, C)

        self._root = MLNode(game_state, None, 1)
        self._model = model

    def _expand_node(self, node_to_expand):
        # Check if this node contains a terminal state before expanding
        if node_to_expand.state.is_terminal():
            return node_to_expand

        child_node = node_to_expand.expand(self._model)
        return child_node

    def _evolve_tree_state(self):
        node_to_act_from = self._select_node(self._root)
        child_node = self._expand_node(node_to_act_from)
        self._backpropogate(child_node, child_node.state.get_reward())