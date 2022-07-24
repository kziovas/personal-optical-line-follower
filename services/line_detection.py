import cv2


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
