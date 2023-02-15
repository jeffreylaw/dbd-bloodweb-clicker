import numpy as np
import math
import os
import signal
import time
import cv2
import pyautogui
import pydirectinput
from pynput import keyboard
from PIL import ImageGrab
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
import yaml, logging, logging.config

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

class BloodwebClicker:

    def __init__(self):
        self.width = None
        self.height = None
        self.get_monitor_res()
        listener = keyboard.Listener(on_press=self.keyboard_listener)
        listener.start()

    """ Click on x, y coordinates and hold for a duration """
    def click_and_hold(self, x, y, duration):
        pydirectinput.moveTo(x, y)
        pydirectinput.mouseDown(x, y)
        pydirectinput.moveTo(0, -9000)
        time.sleep(duration)
        pydirectinput.mouseUp(0, -9000)
        pydirectinput.click()

    """ Get foreground window title """
    def getForegroundWindowTitle(self) -> Optional[str]:
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)

        if buf.value:
            return buf.value
        else:
            return None

    """ Check if dbd is in focus """
    def dbd_in_focus(self):
        if self.getForegroundWindowTitle():
            current_window = self.getForegroundWindowTitle().strip()
            return current_window == "DeadByDaylight"

    """ Listener for keyboard presses
        - ESC key to exit script
    """
    def keyboard_listener(self, key):
        if key == keyboard.Key.esc:
            logger.warning("Exiting script")
            os.kill(os.getpid(), signal.SIGTERM)

    """ Start screenshotting screen, look for circles using OpenCV, and click them """
    def start(self):
        while True:
            try:
                if not self.dbd_in_focus():
                    time.sleep(0.5)
                    continue

                img = ImageGrab.grab()
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img = cv2.medianBlur(img, 5)

                circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50, param2=30, minRadius=40, maxRadius=50)
                detected_circles = np.uint16(np.around(circles))

                for (x, y, r) in detected_circles[0, :]:
                    self.click_and_hold(x, y, 0.8)
            except Exception as exc:
                logging.exception("Exception occured:")

    """ Function for development purposes """
    def dev(self):
        img = cv2.imread("image.png", 0)
        img = cv2.medianBlur(img, 5)

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                param1=50, param2=30, minRadius=40, maxRadius=50)
        detected_circles = np.uint16(np.around(circles))
        for (x, y, r) in detected_circles[0, :]:
            # Draw the outer circle
            cv2.circle(img, (x, y, r), (255, 255, 255), 2)
            # Draw the center circle
            cv2.circle(img, (x, y), 2, (255, 255, 255), 3)

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    """ Get monitor resolution """
    def get_monitor_res(self):
        user32 = windll.user32
        user32.SetProcessDPIAware()
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)


if __name__ == "__main__":
    app = BloodwebClicker()
    logger.info("Initializing Bloodweb Clicker...")
    logger.info("Press esc key to exit script.")
    app.start()
