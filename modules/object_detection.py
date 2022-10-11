from dataclasses import dataclass, field
import numpy as np
import cv2


@dataclass(order=True)
class Stair:
    '''stair objects found on the screenshot'''

    w: int = field(repr=False, init=False, default=87)
    h: int = field(repr=False, init=False, default=47)
    x: int
    y: int

@dataclass
class SearchArea:
    '''segments of the screenshot searched for stair images'''

    dimensions: list
    x         : int
    value     : float = 0.0

class ObjectDetection:
    '''search the screenshot for stair images and find valid stair paths'''

    STAIR_THRESHOLD  = 0.99
    screenshot       = None
    stairs_detected  = list()

    def __init__(self, 
                 stair_images     : list, 
                 horizontal_layers: list, 
                 vertical_layers  : list) -> None:
        '''Initialize needle images and screenshot layers.'''
        
        self.horizontal_layers = horizontal_layers
        self.vertical_layers   = vertical_layers
        self.stair_images      = stair_images

    def update(self, screenshot: list, ) -> None:
        '''Update the current screenshot, bot state, and player's direction.'''

        self.screenshot = screenshot

    def find_needles(self, 
                     haystack  : list, 
                     needles   : list,
                     dimensions: list) -> SearchArea:
        '''Find an object with a value above a threshold in a screenshot segment.'''

        for needle in needles:
            match  = cv2.matchTemplate(haystack, needle, cv2.TM_CCORR_NORMED)
            result = cv2.minMaxLoc(match)
            if result[1] > self.STAIR_THRESHOLD:
                return SearchArea(dimensions, result[3][0], result[1])

    def search_area(self, 
                    dimensions: list, 
                    layer     : int, 
                    whole     : bool = False) -> bool:
        '''Search a specified region for a stair'''

        #   search a screenshot segment
        area_sct = self.screenshot[dimensions[0]: dimensions[1], dimensions[2]: dimensions[3]]
        area     = self.find_needles(area_sct, self.stair_images, dimensions)
        if area is not None:

            #   use the vertical layer of the screenshot segment
            if not whole:
                x_loc = self.vertical_layers.index(dimensions[3])
                self.stairs_detected.append(Stair(x_loc, layer))
                return True

            #   find the vertical layer of the stair if the whole layer is searched
            x_loc = np.searchsorted(self.vertical_layers, area.x, side="right")
            self.stairs_detected.append(Stair(x_loc, layer))
            return True

        return False

    def search_segmented_layer(self, 
                               top   : int, 
                               bottom: int,
                               x_pos : int,
                               layer : int) -> None:
        '''Search a layer of a screenshot in segments for stair objects.'''

        #   Search left screenshot segment
        left_area_dimensions = [top, bottom, self.vertical_layers[x_pos-2], self.vertical_layers[x_pos-1]]
        if self.search_area(left_area_dimensions, layer): return

        #   Search right screenshot segment if necessary
        right_area_dimensions = [top, bottom, self.vertical_layers[x_pos], self.vertical_layers[x_pos+1]]
        if self.search_area(right_area_dimensions, layer): return


    def main(self) -> None:
        '''search each layer algorithmically for stair objects.'''

        self.stairs_detected.clear()

        #   search both sides of the player on the first layer
        self.search_segmented_layer(self.horizontal_layers[11], self.horizontal_layers[12], 4, 12)
        if not self.stairs_detected: return
        for i, layer in reversed(list(enumerate(self.horizontal_layers[1:-1], start=1))):

            #   search the whole layer if stairs skip a layer
            if self.stairs_detected[-1].y-i != 1:
                self.search_area([self.horizontal_layers[i-1], layer, self.vertical_layers[0], self.vertical_layers[7]], i, True)

            #   search both sides of a stair not touching the screen edge
            elif self.stairs_detected[-1].x not in (1, 7):
                self.search_segmented_layer(self.horizontal_layers[i-1], layer, self.stairs_detected[-1].x, i)

            #   search the right side of a stair touching the left screen edge
            elif self.stairs_detected[-1].x == 1:
                self.search_area([self.horizontal_layers[i-1], layer, self.vertical_layers[1], self.vertical_layers[2]], i)

            #   search the left side of a stair touching the right screen edge
            elif self.stairs_detected[-1].x == 7:
                self.search_area([self.horizontal_layers[i-1], layer, self.vertical_layers[5], self.vertical_layers[6]], i)
