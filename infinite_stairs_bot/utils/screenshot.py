from mss import mss
import win32gui as win32
import numpy as np
import cv2


class Screenshot:
    def __init__(self):
        window_handle = win32.FindWindow(None, "BlueStacks App Player")
        client_rect = win32.GetClientRect(window_handle)
        window_location = win32.ClientToScreen(
            window_handle, (client_rect[1], client_rect[0])
        )
        self.win_rect = {
            "left": window_location[0],
            "top": window_location[1],
            "width": client_rect[2],
            "height": client_rect[3],
        }

    def get_screenshot(self):
        with mss() as sct:
            return np.array(sct.grab(self.win_rect))

    def show_window(self, location, img) -> None:
        cv2.imshow("Client Screenshot", img)
        cv2.moveWindow("Client Screenshot", location[0], location[1])
        cv2.waitKey(1)
