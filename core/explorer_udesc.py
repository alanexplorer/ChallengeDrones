# ======== External Modules ========
from threading import Thread
import time
import cv2
from djitellopy import Tello
from imutils.perspective import order_points
import keyboard
from math import sin, cos, sqrt, atan2, pi

ARUCO_SQUARE_SIZE = 0.177800

class TelloExplorer (Thread):
    CLASS_NAME = 'TExplorer'
    def __init__(self) -> None:
        super().__init__()

        self.drone = None
        self.ghostDrone = False

    def run(self, drone: Tello = None):
        drone = self.drone

        if self.ghostDrone:
            print(f'[{self.CLASS_NAME}] (Warning): GHOST_DRONE IS ACTIVE!')
        else:
            if (drone is None):
                print(f'[{self.CLASS_NAME}] Drone Object is None!')
                return
        
        self.imageProcessing = AraucoImageProcessing(self)

        while True:
            if (not self.imageProcessing.is_alive()):
                self.imageProcessing.start()

            #if keyboard.is_pressed("esc"):
            #    print(f'[{self.CLASS_NAME}] Killing Thread!')
            #    break

            time.sleep(0.1)

class AraucoImageProcessing (Thread):
    CLASS_NAME = 'AIP'
    def __init__(self, TelloExplorer: TelloExplorer) -> None:
        super().__init__()

        self.arucoDict = None
        self.arucoParams = None

        self.firstFrameRead = False

        self.TelloExplorer = TelloExplorer
        self.drone = self.TelloExplorer.drone

        self.aruco_init()

    def aruco_init(self):
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.arucoParams = cv2.aruco.DetectorParameters()

    def aruco_detect(self, frameImage) -> tuple:
        corners, ids, _ = cv2.aruco.detectMarkers(frameImage, self.arucoDict, parameters=self.arucoParams)
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, ARUCO_SQUARE_SIZE, self.CAMERA_MATRIX, self.DISTORTION_COEFFICIENTS)
        poses = self.get_pose_coord_aruco(rvecs, tvecs)
        grayFrameImg = cv2.cvtColor(frameImage, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(grayFrameImg, self.arucoDict, parameters=self.arucoParams) # Detect ArUco IDs
        return corners, ids, poses, _

    def find_center_point(self, corners):
        """
        use points that are on the diagonal to calculate the center points
        corners - array of 4 [x,y] arrays.
        corner[0] = [x0,y0]
            corner[0][0] = x0
            corner[0][1] = y0

        """
        center_x = (corners[0][0] + corners[2][0])//2
        center_y = (corners[0][1] + corners[2][1])//2

        return center_x, center_y

    def get_pose_coord_aruco(self, rvecs, tvecs):

        poses = []
        for i in range(rvecs.size):
            yaw = -1 * atan2(tvecs[0][0][0], tvecs[0][0][2])
            p = [rvecs[0], rvecs[1], yaw]
            poses.append(p)

        return poses

    def get_aruco_markers(self, corners, ids, target_id = None) -> tuple:
        all_ordered_corners = []
        all_center_points = []
        all_corners = []
        all_ids = []

        if corners is not None and ids is not None:
            for i, corner in enumerate(corners):
                if target_id is not None and ids[i][0] != target_id:
                    continue

                all_corners.append(corner)
                all_ids.append(ids[i][0])
                ordered_corners = order_points(corner[0])
                all_ordered_corners.append(ordered_corners)
                center_pt_x, center_pt_y = self.find_center_point(ordered_corners)
                all_center_points.append((int(center_pt_x), int(center_pt_y)))
        return all_corners, all_ids, all_ordered_corners, all_center_points

    def run(self, drone: Tello = None):
        drone = self.drone

        if self.TelloExplorer.ghostDrone:
            print(f'[{self.CLASS_NAME}] (GHOST_DRONE): WARNING GHOST_DRONE IS ACTIVE!')
            print(f'[{self.CLASS_NAME}] (GHOST_DRONE): WARNING GHOST_DRONE IS ACTIVE!')
            print(f'[{self.CLASS_NAME}] (GHOST_DRONE): WARNING GHOST_DRONE IS ACTIVE!')
            vidcap = cv2.VideoCapture(0)
            print(f'[{self.CLASS_NAME}] (GHOST_DRONE): Creating WebCam Video Capture!')
            if (not vidcap.isOpened()):
                print(f'[{self.CLASS_NAME}] (GHOST_DRONE): Creating WebCam Video Capture!')
                return
        else:
            if (drone is None):
                print(f'[{self.CLASS_NAME}] Drone Object is None!')
                return

        while True:
            # Breaking Thread if mainThread was killed
            if (not self.TelloExplorer.is_alive()):
                print(f'[{self.CLASS_NAME}] Killing Main Thread!')
                break

            # Getting Current Frame
            try:
                if self.TelloExplorer.ghostDrone:
                    ret, frameImg = vidcap.read()
                else:
                    start = time.time()
                    frameImg = drone.get_frame_read().frame
                    end = time.time()
                    print("Elapsed Time Thread: ", end-start)
            except:
                print(f'[{self.CLASS_NAME}] Frame Read Error!')

            if (not self.firstFrameRead):
                self.firstFrameRead = True
                print(f'[{self.CLASS_NAME}] First Frame was read!')

            try:
                corners, ids, poses, _ = self.aruco_detect(frameImg)
                all_corners, all_ids, all_ordered_corners, all_center_points = self.get_aruco_markers(corners, ids)
                print("corners:", all_corners)
                print("ids:", all_ids)
                print("ordered corners", all_ordered_corners)
                print("center points", all_center_points)
                print("poses:", poses)
            except Exception as e:
                print(e)


            

            # if ids is not None: # If identified any ID
            #     if corners is not None: # And identified their corners
            #         for (marker_corner, marker_id) in zip(corners, ids):
            #             corners = marker_corner.reshape((4, 2))
            #             (topLeft, topRight, bottomRight, bottomLeft) = corners
            time.sleep(1)

if __name__ == "__main__":

    GHOST_DRONE = False

    if (not GHOST_DRONE):
        drone = Tello()
        drone.LOGGER.disabled = True
        drone.connect()
        drone.streamon()
        drone.takeoff()
    else:
        drone = None

    DroneExplorer = TelloExplorer()
    DroneExplorer.ghostDrone = GHOST_DRONE
    DroneExplorer.drone = drone

    DroneExplorer.start()

    time.sleep(10)