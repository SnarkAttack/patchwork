from mcts.action import BaseAction
from .patch import PATCH_S
from .constants import RotationDirection

class PatchworkAction(BaseAction):

    def __init__(self, player_id):
        super().__init__()

        self._player_id = player_id

    @property
    def player_id(self):
        return self._player_id

class AdvanceTokenAction(PatchworkAction):

    def __init__(self, player_id):
        super().__init__(player_id)

    def __str__(self):
        return f"Player {self._player_id} advance token"
    
    def __hash__(self):
        return hash(self.player_id)

class PlacePatchAction(PatchworkAction):

    def __init__(self, player_id, patch, patch_index, dir, index):
        super().__init__(player_id)

        self._patch = patch
        self._patch_index = patch_index
        self._dir = dir
        self._index = index

    @property
    def patch(self):
        return self._patch
    
    @property
    def patch_index(self):
        return self._patch_index
    
    @property
    def dir(self):
        return self._dir
    
    @property
    def index(self):
        return self._index

    def __str__(self):
        return f"Player {self._player_id}, patch {self._patch.id} ({self._patch_index}), dir {self._dir}, index {self._index}"
    
    def __hash__(self):
        return hash((self._player_id, self._patch.id, self._patch_index, self._dir.value, self._index[0], self._index[1]))
    
class PlaceSpecialPatchAction(PlacePatchAction):

    def __init__(self, player_id, index):
        super().__init__(player_id, PATCH_S, 0, RotationDirection.UP, index)