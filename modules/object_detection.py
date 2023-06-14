from dataclasses import dataclass, field
import numpy as np
import cv2


@dataclass(order=True)
class Stair:
    """stair objects found on the screenshot"""

    w: int = field(repr=False, init=False, default=87)
    h: int = field(repr=False, init=False, default=47)
    x: int
    y: int


@dataclass
class SearchArea:
    """segments of the screenshot searched for stair images"""

    dimensions: list
    x: int
    value: float = 0.0


class ObjectDetection:
    """search the screenshot for stair images and find valid stair paths"""

    STAIR_THRESHOLD = 0.99
    screenshot = None
    stairs_detected = list()

    def __init__(
        self, stair_images: list, horizontal_layers: list, vertical_layers: list
    ) -> None:
        """Initialize needle images and screenshot layers."""

        self.horizontal_layers = horizontal_layers
        self.vertical_layers = vertical_layers
        self.stair_images = stair_images

    def update(
        self,
        screenshot: list,
    ) -> None:
        """Update the current screenshot, bot state, and player's direction."""

        self.screenshot = screenshot

    def search_area(self, dimensions: list, layer: int) -> bool:
        """Search a specified region for a stair"""
        area_sct = self.screenshot[
            dimensions[0] : dimensions[1], dimensions[2] : dimensions[3]
        ]
        for needle in self.stair_images:
            match = cv2.matchTemplate(area_sct, needle, cv2.TM_CCORR_NORMED)
            result = cv2.minMaxLoc(match)
            if result[1] > self.STAIR_THRESHOLD:
                x_loc = (
                    np.searchsorted(self.vertical_layers, result[3][0], side="right")
                    if dimensions[2] == self.vertical_layers[0]
                    else self.vertical_layers.index(dimensions[3])
                )
                self.stairs_detected.append(Stair(x_loc, layer))
                return True
        return False

    def main(self) -> None:
        """search each layer algorithmically for stair objects."""
        self.stairs_detected.clear()
        self.search_area(
            [
                self.horizontal_layers[11],
                self.horizontal_layers[12],
                self.vertical_layers[2],
                self.vertical_layers[5],
            ],
            12,
        )
        if not self.stairs_detected:
            return
        for i, layer in reversed(
            list(enumerate(self.horizontal_layers[1:-1], start=1))
        ):
            if self.stairs_detected[-1].y - i != 1:
                self.search_area(
                    [
                        self.horizontal_layers[i - 1],
                        layer,
                        self.vertical_layers[0],
                        self.vertical_layers[7],
                    ],
                    i,
                )
            elif self.stairs_detected[-1].x not in (1, 7):
                self.search_area(
                    [
                        self.horizontal_layers[i - 1],
                        layer,
                        self.vertical_layers[self.stairs_detected[-1].x - 2],
                        self.vertical_layers[self.stairs_detected[-1].x + 1],
                    ],
                    i,
                )
            elif self.stairs_detected[-1].x == 1:
                self.search_area(
                    [
                        self.horizontal_layers[i - 1],
                        layer,
                        self.vertical_layers[0],
                        self.vertical_layers[2],
                    ],
                    i,
                )
            elif self.stairs_detected[-1].x == 7:
                self.search_area(
                    [
                        self.horizontal_layers[i - 1],
                        layer,
                        self.vertical_layers[5],
                        self.vertical_layers[7],
                    ],
                    i,
                )
