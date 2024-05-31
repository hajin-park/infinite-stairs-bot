from utils.screenshot import Screenshot
from utils.assets import Assets
from mtm.inference import MultiTemplateMatch
import concurrent
import cv2


sct = Screenshot()
mtm = MultiTemplateMatch()
assets = Assets(cv2.IMREAD_UNCHANGED)


def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        hits = []
        while True:
            current_sct = sct.get_screenshot()
            result = executor.submit(
                mtm.predict, assets.get_stair_assets(), current_sct
            )
            executor.submit(
                sct.show_window,
                [600, 0],
                sct.get_screenshot(),
            )


if __name__ == "__main__":
    main()
