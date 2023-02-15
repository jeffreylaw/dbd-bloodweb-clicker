import os, signal, time, logging, logging.config
from typing import Optional

import yaml
import numpy as np
import cv2
import pydirectinput
from pynput import keyboard
from PIL import ImageGrab
from ctypes import wintypes, windll, create_unicode_buffer, pointer

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

class BloodwebClicker:

    def __init__(self) -> None:
        self.topleft_x = -1
        self.topleft_y = -1
        self.bottomright_x = -1
        self.bottomright_y = -1

        self.height_res = None
        self.width_res = None
        self.paused = False

        self.get_monitor_res()
        listener = keyboard.Listener(on_press=self.keyboard_listener)
        listener.start()

    """ Click on x, y coordinates and hold for a duration """
    def click_and_hold(self, x, y, duration) -> None:
        pydirectinput.moveTo(x, y)
        pydirectinput.mouseDown(x, y)
        pydirectinput.moveTo(int(((self.bottomright_x[0] - self.topleft_x[0]) / 2)) + self.topleft_x[0], self.topleft_y[1]+10)
        time.sleep(duration)
        pydirectinput.mouseUp(int(((self.bottomright_x[0] - self.topleft_x[0]) / 2)) + self.topleft_x[0], self.topleft_y[1]+10)
        pydirectinput.click()

    """ Get foreground window handle """
    def get_foreground_win_handle(self):
        foreground_window_handle = windll.user32.GetForegroundWindow()
        return foreground_window_handle

    """ Get foreground window title """
    def get_foreground_win_title(self, hdl) -> str:
        window_title_len = windll.user32.GetWindowTextLengthW(hdl)
        buffer = create_unicode_buffer(window_title_len + 1)
        windll.user32.GetWindowTextW(hdl, buffer, window_title_len + 1)

        if not buffer.value:
            return ""

        return buffer.value.strip()

    """ Set x,y coords of upper-left and bottom-right corners of DBD window """
    def set_coords_dbd_window(self, hdl) -> None:
        rect = wintypes.RECT()
        windll.user32.GetWindowRect(hdl, pointer(rect))      

        self.topleft_x = rect.left
        self.topleft_y = rect.top
        self.bottomright_x = rect.right
        self.bottomright_y = rect.bottom

        logger.info(f"Setting -> Topleft: {self.topleft_x},{self.topleft_y}. Bottomright: {self.bottomright_x},{self.bottomright_y}")

    """ Check if dbd is in foreground and set top left, bottom right coordinates """
    def check_for_dbd(self) -> bool:
        foreground_hdl = self.get_foreground_win_handle()
        foreground_win_title = self.get_foreground_win_title(foreground_hdl)

        if foreground_win_title != "DeadByDaylight":
            return False

        if self.topleft_x < 0 or self.topleft_y < 0:   
            return False

        self.set_coords_dbd_window(foreground_hdl)
        return True

    """ Listener for keyboard presses
        - F1 to resume script
        - F2 to pause script
        - F4 to exit script
    """
    def keyboard_listener(self, key) -> None:
        match key:
            case keyboard.Key.f1:
                if self.paused:
                    logger.info("Resuming script")
                    self.paused = False

            case keyboard.Key.f2:
                if not self.paused:
                    logger.info("Pausing script")
                    self.paused = True

            case keyboard.Key.f4:
                hdl = self.get_foreground_win_handle()
                foreground_win_title = self.get_foreground_win_title(hdl)
                if foreground_win_title == "DeadByDaylight":
                    pydirectinput.mouseUp()

                logger.info("Exiting script")
                os.kill(os.getpid(), signal.SIGTERM)

    """ Start screenshotting screen, look for circles using OpenCV, and click them """
    def start(self) -> None:
        while True:
            if self.paused:
                continue

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
                if circles is not None:
                    detected_circles = np.uint16(np.around(circles))
                    for (x, y, r) in detected_circles[0, :]:
                        if self.topleft_x[0] <= x <= self.bottomright_x[0] and self.topleft_y[1] <= y <= self.bottomright_y[1]:
                            self.click_and_hold(x, y, 0.7)
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
    logger.info("Press F4 key to exit script.")
    app.start()
