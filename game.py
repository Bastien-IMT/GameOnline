import numpy as np

from boat import Boat
from game_data import *


class Game:
    def __init__(self):
        self.my_grid = np.full(GRID_SIZE, GridCellType.water.value, dtype=int)
        self.my_guessed = np.full(GRID_SIZE, GridCellType.water.value, dtype=int)

        self.my_boats = []

    def place_one_boat(self, boat_type: BoatType, pos_head: tuple, orientation: Orientation):
        if self.check_correct_boat_location(boat_type, pos_head, orientation):
            self.my_boats.append(Boat(boat_type, pos_head, orientation))

            if orientation == Orientation.horizontal:
                for i in range(boat_type.value):
                    self.my_grid[pos_head[1]][pos_head[0] + i] = GridCellType.boat.value

            elif orientation == Orientation.vertical:
                for i in range(boat_type.value):
                    self.my_grid[pos_head[1] + i][pos_head[0]] = GridCellType.boat.value

    def check_correct_boat_location(self, boat_type: BoatType, pos_head: tuple, orientation: Orientation):
        """
        Check if the boat's location in the grid is correct
        :param boat_type: BoatType enum
        :param pos_head: tuple (x, y)
        :param orientation: Orientation enum
        :return: Boolean
        """
        result = False

        if orientation == Orientation.horizontal:
            # make sure boat fits in the grid
            if pos_head[0] + boat_type.value - 1 <= GRID_SIZE[0] - 1:
                if GRID_SIZE[0] - 1 >= pos_head[0] >= 0 and GRID_SIZE[1] - 1 >= pos_head[1] >= 0:
                    # make sure boat does not cross another boat
                    free_space = True
                    for i in range(boat_type.value):
                        if self.my_grid[pos_head[1]][pos_head[0] + i] != GridCellType.water:
                            free_space = False
                            break
                    if free_space:
                        result = True

        elif orientation == Orientation.vertical:
            # make sure boat fits in the grid
            if pos_head[1] + boat_type.value - 1 <= GRID_SIZE[1] - 1:
                if GRID_SIZE[0] - 1 >= pos_head[0] >= 0 and GRID_SIZE[1] - 1 >= pos_head[1] >= 0:
                    # make sure boat does not cross another boat
                    free_space = True
                    for i in range(boat_type.value):
                        if self.my_grid[pos_head[1] + i][pos_head[0]] != GridCellType.water:
                            free_space = False
                            break
                    if free_space:
                        for i in range(boat_type.value):
                            result = True
        return result

    def attack_enemy(self, pos: tuple):
        if self.correct_attack_location(pos):
            self.my_guessed[pos[1]][pos[0]] = GridCellType.guess

    def correct_attack_location(self, pos: tuple):
        res = False
        if (0 <= pos[0] < GRID_SIZE[0]) and (0 <= pos[1] < GRID_SIZE[1]):  # in the grid
            if self.my_guessed[pos[1]][pos[0]] == GridCellType.water:
                res = True
        return res
