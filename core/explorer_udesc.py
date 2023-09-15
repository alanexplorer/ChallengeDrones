# ======== External Modules ========
from threading import Thread
import time
import cv2
from djitellopy import Tello

class AraucoImageProcessing (Thread):
    CLASS_NAME = 'AIP'
    def __init__(self) -> None:
        super().__init__()

        self.arucoDict = None
        self.arucoParams = None

        self.drone = None

        self.aruco_init()

    def aruco_init(self):
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.arucoParams = cv2.aruco.DetectorParameters()

    def run(self, drone: Tello = None):
        drone = self.drone
        if drone is None:
            print(f'[{self.CLASS_NAME}] Drone Object is None!')
            return

        while True:
            # Getting Current Frame
            frame = drone.get_frame_read().frame

            corners, ids, _ = cv2.aruco.detectMarkers(frame, self.arucoDict, parameters=self.arucoParams)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters=self.arucoParams) # Detect ArUco IDs

            print(corners, ids, _)

            # if ids is not None: # If identified any ID
            #     if corners is not None: # And identified their corners
            #         for (marker_corner, marker_id) in zip(corners, ids):
            #             corners = marker_corner.reshape((4, 2))
            #             (topLeft, topRight, bottomRight, bottomLeft) = corners
            time.sleep(1)

class TelloExplorer (Thread):
    CLASS_NAME = 'TExplorer'
    def __init__(self) -> None:
        super().__init__()
        self.drone = None

    def run(self, drone: Tello = None):
        drone = self.drone
        if drone is None:
            print(f'[{self.CLASS_NAME}] Drone Object is None!')
            return

        while True:
            self.imageProcessing = AraucoImageProcessing()
            self.imageProcessing.drone = self.drone
            self.imageProcessing.start()

            time.sleep(1)

if __name__ == "__main__":

    drone = Tello()
    drone.LOGGER.disabled = True
    drone.connect()
    drone.takeoff()

    DroneExplorer = TelloExplorer()
    DroneExplorer.drone = drone

    DroneExplorer.start()