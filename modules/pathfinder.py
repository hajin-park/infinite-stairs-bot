class PathFinder:
    '''Pathfind by filling in missing layers from a list of detected stairs.'''

    screenshot = None
    state = None
    left = True
    stairs_detected = list()
    stairs_connected = list()
    actions = list()

    def update(self, left: bool, stairs_detected: list) -> None:
        '''Update the current screenshot, bot state, and player's direction.'''

        self.left = left
        self.stairs_detected = stairs_detected

    def fill_edge(self, stair):
        '''Fill in two layers off the screen'''

        if (stair.x not in (1, 7)):
            return True

        #   stair is on the left screen edge
        elif (stair.x == 1):
            self.stairs_connected.append([stair.x-1, stair.y-1])
            self.stairs_connected.append([stair.x-2, stair.y-2])

        #   stair is on the right screen edge
        elif (stair.x == 7):
            self.stairs_connected.append([stair.x+1, stair.y-1])
            self.stairs_connected.append([stair.x+2, stair.y-2])

    def fill_last(self, stair, next_stair):
        self.stairs_connected.append([next_stair.x, next_stair.y])
        self.fill_edge(stair)

    def fill_zero(self, delta_x, stair, next_stair, next_is_last):
        if (delta_x not in (-1, 1)):
            return True

        if next_is_last:
            self.fill_last(stair, next_stair)

    def fill_one(self, delta_x, stair, next_stair, next_is_last):
        if (delta_x not in (-2, 2, 0)):
            return True

        #   current stair is next to next stair
        elif (delta_x in (-2, 2)):
            self.stairs_connected.append([stair.x-(delta_x/2), stair.y-1])

        #   current stair is under next stair
        elif (stair.x in (1, 5)):
            self.stairs_connected.append([stair.x-1, stair.y-1])

        #   current stair is under next stair
        elif (stair.x in (3, 7)):
            self.stairs_connected.append([stair.x+1, stair.y-1])

        else:
            return True

        if next_is_last:
            self.fill_last(stair, next_stair)

    def fill_two(self, delta_x, stair, next_stair, next_is_last):
        if (delta_x not in (-3, 3)):
            return True

        #   bottom stair is left of top stair
        elif (delta_x == -3):
            self.stairs_connected.append([stair.x+1, stair.y-1])
            self.stairs_connected.append([stair.x+2, stair.y-2])

        #   bottom stair is right of top stair
        elif (delta_x == 3):
            self.stairs_connected.append([stair.x-1, stair.y-1])
            self.stairs_connected.append([stair.x-2, stair.y-2])

        if next_is_last:
            self.fill_last(stair, next_stair)

    def fill_path(self) -> None:
        '''Pathfind and fill in empty layers between detected stairs.'''

        if (self.stairs_detected[0].y != 12 or self.stairs_detected[0].x not in (3, 5)):
            return

        for (i, stair) in enumerate(self.stairs_detected[:-1], start=1):
            next_stair = self.stairs_detected[i]
            next_is_last = self.stairs_detected[-1] == next_stair
            delta_x = stair.x - next_stair.x
            delta_y = stair.y - next_stair.y

            self.stairs_connected.append([stair.x, stair.y])

            #   end pathfinding if there an empty layer above a certain point
            if (delta_y != 1 and stair.y < 7):
                return

            elif (delta_y == 1):
                if self.fill_zero(delta_x, stair, next_stair, next_is_last):
                    return

            elif (delta_y == 2):
                if self.fill_one(delta_x, stair, next_stair, next_is_last):
                    return

            elif (delta_y == 3):
                if self.fill_two(delta_x, stair, next_stair, next_is_last):
                    return

            #   end pathfinding if there are more than two consecutive empty layers
            else:
                return self.fill_edge(stair)

    def next_action(self, current_stair: float, next_stair: int) -> str:
        '''Queue an action for two consecutive stairs.'''

        button = ''

        if (next_stair < current_stair):
            button = 'right' if self.left else 'left'
        elif (next_stair > current_stair):
            button = 'left' if self.left else 'right'
        if (button == 'left'):
            self.left = not self.left

        return button

    def queue_actions(self) -> None:
        '''Queue actions based on the path created.'''

        if self.stairs_connected:

            self.actions.append(self.next_action(
                4, self.stairs_connected[0][0]))
            for i in range(len(self.stairs_connected)-1):

                current_stair = self.stairs_connected[i][0]
                next_stair = self.stairs_connected[i+1][0]
                self.actions.append(self.next_action(
                    current_stair, next_stair))

    def main(self) -> None:
        '''main loop to reset and generate a new path'''

        self.stairs_connected.clear()
        self.actions.clear()
        if self.stairs_detected:
            self.fill_path()
            self.queue_actions()
