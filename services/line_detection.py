import numpy as np
import cv2, PIL
import matplotlib.pyplot as plt
import matplotlib as mpl
import PIL.Image


class Camera:
    def __init__(self, camera=1):
        self.camera = camera
        self.cap = cv2.VideoCapture(self.camera)

    def take_frame(self):
        ret, frame = self.cap.read()
        return frame

    def stop(self):
        self.cap.release()


class ShowImage:
    def preview(self, frame):
        cv2.imshow("frame", frame)
        cv2.waitKey(1)

    def clear(self):
        cv2.destroyAllWindows()


class RobotCentering:
    def __init__(self, width=640):
        self.width = width
        self.step = int(width / 5)
        self.w1 = self.step * 2
        self.w2 = self.step * 3

    def direction(self, posx):
        if posx > 0 and posx < self.w1:
            print("Go Right")
            return 2
        elif posx > self.w2 and posx < self.width:
            print("Go Left")
            return 1
        elif posx == 0:
            print("No detection")
            return -1
        else:
            print("Stay")
            return 0


class RobotFollowing:
    def __init__(self, width=640):
        self.width = width
        self.max = int(width / 2)

    def direction(self, rx):
        if rx < self.max and rx > 0:
            print("Forward")
            return 1
        elif rx > (self.max + 30):
            print("Back")
            return 2
        elif rx == 0:
            print("No detection")
            return -1
        else:
            print("Stay")
            return 0


class LineDetector:
    def __init__(self, width=640, height=480, w=280, h=150):
        self.width = width
        self.height = height
        self.cx = 0
        self.cy = 0
        self.x1 = max(0, int((self.width / 2) - (w / 2)))
        self.x2 = min(int((self.width / 2) + (w / 2)), self.width)
        self.y1 = max(0, int((self.height / 2) - (h / 2)))
        self.y2 = min(int((self.height / 2) + (h / 2)), self.height)

    def detect_line(self, frame):
        crop_img = frame[self.y1 : self.y2, self.x1 : self.x2]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                self.cx = int(M["m10"] / M["m00"])
                self.cy = int(M["m01"] / M["m00"])
                cv2.line(crop_img, (self.cx, 0), (self.cx, self.height), (255, 0, 0), 1)
                cv2.line(crop_img, (0, self.cy), (self.width, self.cy), (255, 0, 0), 1)
                cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)
            else:
                self.cx = 0
                self.cy = 0
        else:
            self.cx = 0
            self.cy = 0

        return crop_img

    def get_pos(self):
        return self.cx, self.cy
