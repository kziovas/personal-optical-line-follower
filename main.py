from services import (
    Camera,
    LineDetector,
    ShowImage,
)
from time import sleep

if __name__ == "__main__":
    camera = Camera()
    display = ShowImage()
    line_detector = LineDetector()

    while True:
        frame = camera.take_frame()
        crop_image = line_detector.detect_line(frame=frame)
        display.preview(frame=crop_image)
        pos: tuple = line_detector.get_pos()
        print(pos)
