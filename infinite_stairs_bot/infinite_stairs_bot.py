from utils.window_capture import WindowCapture
from mtm.inference import MultiTemplateMatch
import os
import cv2


capture = WindowCapture()
mtm = MultiTemplateMatch()

stair_images = [
    cv2.imread(
        os.path.join(os.getcwd(), "mtm", "templates", "green_brick_stair.png"),
        cv2.IMREAD_UNCHANGED,
    ),
    cv2.imread(
        os.path.join(os.getcwd(), "mtm", "templates", "gold_stair.png"),
        cv2.IMREAD_UNCHANGED,
    ),
    cv2.imread(
        os.path.join(os.getcwd(), "mtm", "templates", "gem_stair.png"),
        cv2.IMREAD_UNCHANGED,
    ),
]

while True:
    result = mtm.predict(
        [
            ("green_brick_stair", stair_images[0]),
            ("gold_stair", stair_images[0]),
            ("gem_stair", stair_images[0]),
        ],
        capture.get_screenshot(),
    )
    capture.show_window([600, 0], result)
