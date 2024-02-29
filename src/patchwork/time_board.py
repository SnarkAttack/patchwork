from .constants import PLAYER1, PLAYER2

class TimeBoard:

    def __init__(self,
                 track_len = 54,
                 available_special_patches = [19, 25, 31, 43, 49],
                 button_income = [4, 10, 16, 22, 28, 34, 40, 52, 1000]):
        
        self._locations = {
            PLAYER1: 0, 
            PLAYER2: 0
        }

        self._incomes_received = {
            PLAYER1: 0, 
            PLAYER2: 0
        }

        # Players start on the first of 54 spaces
        self._track_len = track_len

        # The numbers in these arrays are the space BEFORE the corresponding
        # patch/income spot, so we can check if a player's current space has
        # exceeded an available location
        self._available_special_patches = available_special_patches
        self._button_income = button_income

        self._tiebreaker = None

    def are_players_stacked(self):
        return self._locations[PLAYER1] == self._locations[PLAYER2]

    def _perform_player_stacking(self, player_id):
        if self._locations[PLAYER1] == self._locations[PLAYER2]:
            self._tiebreaker = player_id
        else:
            self._tiebreaker = 0

    def is_player_done(self, player_id):
        return self._locations[player_id] >= self._track_len
    
    def determine_spaces_to_advance(self, player_id):
        if player_id == PLAYER1:
            return self._locations[PLAYER2] - self._locations[PLAYER1] + 1
        else:
            return self._locations[PLAYER1] - self._locations[PLAYER2] + 1

    def move_player_forward(self, player_id, num_spaces):
        self._locations[player_id] += num_spaces

        incomes_received = 0
        patches_received = 0

        while self._locations[player_id] > self._button_income[self._incomes_received[player_id]]:
            self._incomes_received[player_id] += 1
            incomes_received += 1

        # Check if we get a patch
        while len(self._available_special_patches) > 0 and self._locations[player_id] > self._available_special_patches[0]:
            self._available_special_patches.pop(0)
            patches_received += 1

        self._perform_player_stacking(player_id)

        return (incomes_received, patches_received)

    def determine_next_player(self):
        if self.are_players_stacked():
            return self._tiebreaker
        else:
            if self._locations[PLAYER1] < self._locations[PLAYER2]:
                return PLAYER1
            else:
                return PLAYER2
