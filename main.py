'''Python OpenCV Infinite Stairs Bot'''


from modules.bot import Bot
from modules.images import Images
from modules.object_detection import ObjectDetection
from modules.pathfinder import PathFinder
from modules.windowcapture import WindowCapture
import keyboard as kb
from time import sleep


kb.wait('s')

#   initialize modules
images = Images()
sct = WindowCapture()
detector = ObjectDetection(
    images.stair_images, sct.horizontal_layers, sct.vertical_layers)
pathfinder = PathFinder()
bot = Bot(images.start_images, images.stop_images)


def main():

    sct.start()  # start screenshot thread
    while sct.screenshot is None:
        sleep(0)  # wait for the first screenshot
    bot.update_screenshot(sct.screenshot)  # give the bot the first screenshot
    bot.start()  # start bot thread

    while True:

        #   update threads
        bot.update_screenshot(sct.screenshot)

        #   update object detector
        detector.update(sct.screenshot)
        detector.main()

        pathfinder.update(bot.left, detector.stairs_detected)
        pathfinder.main()

        sct.update(pathfinder.stairs_connected)

        #   update bot actions
        if (bot.state == 'READY'):
            bot.update_actions(pathfinder.actions)

        #   terminate the bot with a "q" keypress
        if kb.is_pressed('q'):
            sct.stop()
            bot.stop()
            break


if __name__ == '__main__':
    main()
