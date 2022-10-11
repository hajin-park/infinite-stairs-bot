from mss import mss
from threading import Thread, Lock
import win32gui as win32
import numpy as np
import cv2


class WindowCapture:
    stopped = True
    lock = None
    screenshot = None
    temp_sct = None
    window_rect = None
    sct_rect = None
    rects = list()
    sct = mss()

    def __init__(self):
        window_handle = win32.FindWindow(None, 'BlueStacks App Player')
        client_rect = win32.GetClientRect(window_handle)
        window_location = win32.ClientToScreen(
            window_handle, (client_rect[1], client_rect[0]))
        self.win_rect = {
            'left': window_location[0],
            'top': window_location[1],
            'width': client_rect[2],
            'height': client_rect[3]
        }
        self.sct_rect = {
            'left': self.win_rect['left'],
            'top': self.win_rect['top']+120,
            'width': self.win_rect['width'],
            'height': 564
        }
        self.sct_x_loc = self.win_rect['left']+self.win_rect['width']
        self.sct_y_loc = int(
            self.win_rect['top']+self.win_rect['height']*0.11111)-30
        self.horizontal_layers = [y for y in range(
            0, self.sct_rect['height']+1, 47)]
        self.vertical_layers = [
            0]+[x for x in range(66, self.sct_rect['width'], 87)]+[self.sct_rect['width']]
        self.lock = Lock()

    def update(self, rects):
        self.lock.acquire()
        self.rects = rects
        self.lock.release()

    def get_screenshot(self):
        return np.array(self.sct.grab(self.sct_rect))

    def draw_rectangles(self):
        self.temp_sct = self.screenshot
        for (x, y) in self.rects:
            if (x > 0 and x < 8):
                cv2.rectangle(
                    self.temp_sct,
                    (self.vertical_layers[int(x-1)],
                     self.horizontal_layers[int(y-1)]),
                    (self.vertical_layers[int(x)],
                     self.horizontal_layers[int(y)]),
                    (0, 0, 255),
                    4
                )

    def show_window(self, location) -> None:
        cv2.imshow('Screen Shot', self.temp_sct)
        cv2.moveWindow('Screen Shot', location[0], location[1])
        cv2.waitKey(1)

    def start(self):
        self.stopped = False
        thread = Thread(target=self.run)
        thread.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            self.lock.acquire()
            self.screenshot = self.get_screenshot()
            self.lock.release()

            self.draw_rectangles()
            self.show_window([self.sct_x_loc, self.sct_y_loc])

        cv2.destroyAllWindows()
