from typing import List, Tuple


class PathFinder:
    """Pathfind by filling in missing layers from a list of detected stairs."""

    def __init__(self):
        self.left = True
        self.stairs_detected: List[Tuple[int, int]] = []
        self.stairs_connected: List[Tuple[int, int]] = []
        self.actions: List[str] = []

    def update(self, left: bool, stairs_detected: List[Tuple[int, int]]) -> None:
        """Update the current screenshot, bot state, and player's direction."""
        self.left = left
        self.stairs_detected = stairs_detected

    def fill_stairs(self, delta_x: int, delta_y: int, stair: Tuple[int, int]) -> None:
        """Fill in the stairs based on the difference in x and y coordinates of the current and next stairs."""
        if delta_y == 1 and delta_x in (-1, 1):
            if delta_x == -1:
                self.stairs_connected.append((stair[0] + 1, stair[1] - 1))
            else:
                self.stairs_connected.append((stair[0] - 1, stair[1] - 1))
        elif delta_y == 2 and delta_x in (-2, 2, 0):
            self.stairs_connected.append((stair[0] - delta_x // 2, stair[1] - 1))
        elif delta_y == 3 and delta_x in (-3, 3):
            self.stairs_connected.append((stair[0] + delta_x // 3, stair[1] - 1))
            self.stairs_connected.append((stair[0] + 2 * delta_x // 3, stair[1] - 2))

    def fill_path(self) -> None:
        """Pathfind and fill in empty layers between detected stairs."""
        if self.stairs_detected[0][1] != 12 or self.stairs_detected[0][0] not in (3, 5):
            return

        for i, stair in enumerate(self.stairs_detected[:-1]):
            next_stair = self.stairs_detected[i + 1]
            delta_x = stair[0] - next_stair[0]
            delta_y = stair[1] - next_stair[1]

            self.stairs_connected.append(stair)

            if delta_y != 1 and stair[1] < 7:
                return
            else:
                self.fill_stairs(delta_x, delta_y, stair)

    def next_action(self, current_stair: float, next_stair: int) -> str:
        """Queue an action for two consecutive stairs."""
        button = ""
        if next_stair < current_stair:
            button = "right" if self.left else "left"
        elif next_stair > current_stair:
            button = "left" if self.left else "right"
        if button == "left":
            self.left = not self.left

        return button

    def queue_actions(self) -> None:
        """Queue actions based on the path created."""

        if self.stairs_connected:
            self.actions.append(self.next_action(4, self.stairs_connected[0][0]))
            for i in range(len(self.stairs_connected) - 1):
                current_stair = self.stairs_connected[i][0]
                next_stair = self.stairs_connected[i + 1][0]
                self.actions.append(self.next_action(current_stair, next_stair))

    def main(self) -> None:
        """main loop to reset and generate a new path"""

        self.stairs_connected.clear()
        self.actions.clear()
        if self.stairs_detected:
            self.fill_path()
            self.queue_actions()
