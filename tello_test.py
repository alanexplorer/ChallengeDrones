from droneblocks.DroneBlocksTello import DroneBlocksTello
from droneblocksutils import aruco_utils
import cv2
tello = DroneBlocksTello()


tello.connect()
# tello.takeoff()

# b = tello.get_battery()

# print(b)

# tello.move_up(100)
# tello.rotate_counter_clockwise(90)
# tello.move_forward(100)

print("re1")
frame = tello.get_frame_read().frame
print("re2")


result = aruco_utils.detect_markers_in_image(frame)

# print(result)

# tello.land()
tello.clear_everything()