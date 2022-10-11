from time import perf_counter
from threading import Thread, Lock
import cv2
import pydirectinput as pdi


class Bot:
    pdi.PAUSE       = 0.02
    TIME_THRESHOLD  = 0.3
    START_THRESHOLD = 0.95
    STOP_THRESHOLD  = 0.98
    time_waited     = 0.0
    lock            = None
    state           = None
    screenshot      = None
    left            = True
    actions         = list()

    def __init__(self, start_images, stop_images):
        self.start_images = start_images
        self.stop_images  = stop_images
        self.state        = 'STOP'
        self.lock         = Lock()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def update_actions(self, actions):
        self.lock.acquire()
        self.actions = actions
        self.lock.release()

    def update_state(self, state):
        self.lock.acquire()
        self.actions.clear()
        self.state = state
        self.time_waited = perf_counter()
        self.lock.release()

    def find_needles(self, haystack, needles, threshold):
        for needle in needles:
            result  = cv2.matchTemplate(haystack, needle, cv2.TM_CCORR_NORMED)
            max_val = cv2.minMaxLoc(result)[1]
            if max_val > threshold:
                return True
   
    def check_screen(self, images, state, threshold):
        result = self.find_needles(self.screenshot, images, threshold)
        if result: self.update_state(state)

    def stop_state(self):
        self.check_screen(self.start_images, 'START', self.START_THRESHOLD)

    def start_state(self):
        pdi.press('right')
        self.left = True
        self.update_state('ACTIVE')

    def ready_state(self):
        if self.actions:
            self.lock.acquire()
            for action in self.actions: pdi.press(action)
            if (self.actions.count('left') % 2): self.left = not self.left
            self.lock.release()
            self.update_state('ACTIVE')

    def active_state(self):
        self.check_screen(self.stop_images, 'STOP', self.STOP_THRESHOLD)
        if (perf_counter() - self.time_waited > self.TIME_THRESHOLD):
            self.update_state('READY')

    def start(self):
        self.stopped = False
        thread = Thread(target=self.run)
        thread.start()

    def stop(self):
        self.stopped = True

    def run(self):
        self.time_waited = perf_counter()
        while not self.stopped:
            print(self.state)
            self.BOT_STATES[self.state](self)

    BOT_STATES = {
        'STOP'  : stop_state,
        'START' : start_state,
        'ACTIVE': active_state,
        'READY' : ready_state
    }
