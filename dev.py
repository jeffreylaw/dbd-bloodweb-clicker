import numpy as np
import math
import os
import signal
import time
import cv2
import pyautogui
import pydirectinput
import logging
from pynput import keyboard
from PIL import ImageGrab
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer


logging.basicConfig(filename="app.log", filemode="a", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class BloodwebClicker:

    def __init__(self):
        print("Press right-control key to exit script")
        print("Initializing Bloodweb Clicker...")
        self.width = None
        self.height = None
        self.get_monitor_res()
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def click_and_hold(self, x, y, duration):
        pydirectinput.moveTo(x, y)
        pydirectinput.mouseDown(x, y)
        pydirectinput.moveTo(0, -9000)
        time.sleep(duration)
        pydirectinput.mouseUp(0, -9000)
        pydirectinput.click()

    """ Manually read image using cv2 using an absolute path """

    def manually_read_image(self, filename):
        img = cv2.imread(filename, 0)
        return img

    def start(self, mode):
        while True:
            try:
                if mode == "dev-img":
                    img = cv2.imread("image.png", 0)
                    img = cv2.medianBlur(img, 5)

                    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                            param1=50, param2=30, minRadius=40, maxRadius=50)
                    detected_circles = np.uint16(np.around(circles))
                    for i in detected_circles[0, :]:
                        # Outer circle
                        cv2.circle(img, (i[0], i[1]), i[2], (255, 255, 255), 2)

                        # Center
                        cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 3)

                    cv2.imshow('img', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    break
                elif mode == "dev":
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
                elif mode == "prod":
                    if not self.dbd_in_focus():
                        time.sleep(0.5)
                        continue
                    img = ImageGrab.grab()
                    img = np.array(img)
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    img = cv2.medianBlur(img, 5)

                if not self.dbd_in_focus:
                    continue
                circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                           param1=50, param2=30, minRadius=40, maxRadius=50)
                detected_circles = np.uint16(np.around(circles))

                for (x, y, r) in detected_circles[0, :]:
                    if x > (self.width * 0.7):
                        continue

                    match_found = False
                    for i in range(361):
                        circle_x = int(r * math.cos(i) + x)
                        circle_y = int(r * math.sin(i) + y)
                        if pyautogui.pixelMatchesColor(circle_x, circle_y, (146, 138, 109), tolerance=20):
                            match_found = True
                            break
                    if match_found:
                        if not self.dbd_in_focus:
                            continue
                        self.click_and_hold(x, y, 0.8)
            except Exception as e:
                print(e)
                # logging.error("Exception: ", e)

    """ Check if dbd is in focus """
    def dbd_in_focus(self):
        current_window = self.getForegroundWindowTitle().strip()
        return current_window == "DeadByDaylight"

    # https://stackoverflow.com/questions/10266281/obtain-active-window-using-python
    def getForegroundWindowTitle(self) -> Optional[str]:
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)

        if buf.value:
            return buf.value
        else:
            return None

    def on_press(self, key):
        if key == keyboard.Key.ctrl_l:
            print("Exiting script")
            os.kill(os.getpid(), signal.SIGTERM)

    def get_monitor_res(self):
        user32 = windll.user32
        user32.SetProcessDPIAware()
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)


if __name__ == "__main__":
    app = BloodwebClicker()
    app.start(mode="dev")
