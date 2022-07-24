from services import Camera, LineDetector, ShowImage, PID
from time import sleep, time


if __name__ == "__main__":
    camera = Camera()
    display = ShowImage()
    line_detector = LineDetector()
    controller = PID(KP=1, KI=0.3)

    while True:
        start_time = time()
        frame = camera.take_frame()
        crop_image = line_detector.detect_line(frame=frame)
        display.preview(frame=crop_image)
        pos: tuple = line_detector.get_pos()
        end_time = time()
        response = controller.calculate_response(
            actual_value=pos[0], start_time=start_time, end_time=end_time
        )
        print(f"Current road position: {pos}")
        print(f"PID output: {response}")
        sleep(0.2)
