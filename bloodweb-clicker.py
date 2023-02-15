import os, signal, time, logging, logging.config
from typing import Optional

import yaml
import numpy as np
import cv2
import pydirectinput
import pyautogui
from pynput import keyboard
from PIL import ImageGrab
from ctypes import wintypes, windll, create_unicode_buffer, pointer

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

class BloodwebClicker:

    def __init__(self) -> None:
        self.top_l = (-1, -1)
        self.bottom_r = (-1, -1)
        self.height_res = None
        self.width_res = None
        self.get_monitor_res()
        listener = keyboard.Listener(on_press=self.keyboard_listener)
        listener.start()

    """ Click on x, y coordinates and hold for a duration """
    def click_and_hold(self, x, y, duration) -> None:
        pydirectinput.moveTo(x, y)
        pydirectinput.mouseDown(x, y)
        pydirectinput.moveTo(int(((self.bottom_r[0] - self.top_l[0]) / 2)) + self.top_l[0], self.top_l[1]+10) # type: ignore
        time.sleep(duration)
        pydirectinput.mouseUp(int(((self.bottom_r[0] - self.top_l[0]) / 2)) + self.top_l[0], self.top_l[1]+10) # type: ignore
        pydirectinput.click()

    """ Check if dbd is in foreground and set top left, bottom right coordinates """
    def check_for_dbd(self) -> bool:
        foreground_window_handle = windll.user32.GetForegroundWindow()
        window_title_len = windll.user32.GetWindowTextLengthW(foreground_window_handle)
        buffer = create_unicode_buffer(window_title_len + 1)
        windll.user32.GetWindowTextW(foreground_window_handle, buffer, window_title_len + 1)

        if not buffer.value and buffer.value.strip() != "DeadByDaylight":
            return False
            
        rect = wintypes.RECT()
        windll.user32.GetWindowRect(foreground_window_handle, pointer(rect))        

        if rect.left < 0: # type: ignore    
            return False

        self.top_l = (rect.left, rect.top)
        self.bottom_r = (rect.right, rect.bottom)
        # print(f"Topleft: {rect.left},{rect.top}. Bottomright: {rect.right},{rect.bottom}")
        return True


    """ Listener for keyboard presses
        - ESC key to exit script
    """
    def keyboard_listener(self, key) -> None:
        if key == keyboard.Key.esc:
            logger.info("Exiting script")
            os.kill(os.getpid(), signal.SIGTERM)

    """ Start screenshotting screen, look for circles using OpenCV, and click them """
    def start(self) -> None:
        while True:
            try:
                if not self.check_for_dbd():
                    time.sleep(0.5)
                    continue

                img = ImageGrab.grab()
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img = cv2.medianBlur(img, 5)

                circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50, param2=30, minRadius=40, maxRadius=50)
                if circles:
                    detected_circles = np.uint16(np.around(circles))
                    for (x, y, r) in detected_circles[0, :]:
                        if self.top_l[0] <= x <= self.bottom_r[0] and self.top_l[1] <= y <= self.bottom_r[1]:
                            self.click_and_hold(x, y, 1.1)
            except Exception as exc:
                logging.exception("Exception occured:")

    """ Function for development purposes """
    def dev(self) -> None:
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
    def get_monitor_res(self) -> None:
        user32 = windll.user32
        user32.SetProcessDPIAware()
        self.width_res = user32.GetSystemMetrics(0)
        self.height_res = user32.GetSystemMetrics(1)


if __name__ == "__main__":
    app = BloodwebClicker()
    logger.info("Initializing Bloodweb Clicker...")
    logger.info("Press esc key to exit script.")
    app.start()
