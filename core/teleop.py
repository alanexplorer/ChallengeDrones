# ============== External Modules ==============
from djitellopy import Tello
from threading import Thread
import time
import keyboard
# ==============================================
class TelloTeleop (Thread):
    CLASS_NAME = 'TTeleop'
    def __init__(self) -> None:
        super().__init__()
        self.drone = None
        
    def run(self, drone: Tello = None):
        drone = self.drone

        if drone is None:
            print(f'[{self.CLASS_NAME}] Drone is None object!')
            return
        if (not drone.is_flying):
            print(f'[{self.CLASS_NAME}] Drone is not flying!')
            return

        while(True):
            time.sleep(0.01)
            if keyboard.is_pressed("space"):
                drone.emergency()
                print(f'[{self.CLASS_NAME}] Emergency pressed!')
            if keyboard.is_pressed("enter"):
                drone.land()
                print(f'[{self.CLASS_NAME}] Land Button pressed!')
            if keyboard.is_pressed("esc"):
                drone.end()
                print(f'[{self.CLASS_NAME}] Drone End Tello Object!')
                return

            foward_backward_vel = 0
            if keyboard.is_pressed("down"):
                foward_backward_vel += -50 # Backward
            if keyboard.is_pressed("up"):
                foward_backward_vel += 50 # Foward

            left_right_vel = 0
            if keyboard.is_pressed("right"):
                left_right_vel += 50 # Right
            if keyboard.is_pressed("left"):
                left_right_vel += -50 # Left

            yaw_vel = 0
            if keyboard.is_pressed("q"):
                yaw_vel += -50 # yaw +
            if keyboard.is_pressed("e"):
                yaw_vel += 50 # yaw +

            up_down_vel = 0
            if keyboard.is_pressed("shift"):
                up_down_vel += 50 # Up
            if keyboard.is_pressed("ctrl"):
                up_down_vel += -50 # Down

            if keyboard.is_pressed("alt"):
                if (not drone.is_flying):
                    drone.takeoff()

            drone.send_rc_control(
                left_right_velocity=left_right_vel,
                forward_backward_velocity=foward_backward_vel,
                yaw_velocity=yaw_vel,
                up_down_velocity = up_down_vel
                )


if __name__ == "__main__":
    tteleop = TelloTeleop()

    drone = Tello()
    drone.LOGGER.disabled = True
    drone.connect()
    drone.takeoff()

    # Initializing Threading
    tteleop.drone = drone
    tteleop.start()

    while True:
        print('teste')
        time.sleep(1)
