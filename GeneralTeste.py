import cv2
import threading
import time
from djitellopy import Tello
from timeit import default_timer as timer #Measure Time (Debug)

def initialize():
	drone = Tello()
	drone.connect()
	drone.streamon()
	#cv2.namedWindow("Tello") # Stream window
	return drone # Initialize drone

def frame_thread(): # Função de atualização global do frame
	
    global frame, tello
    while True:
		
        start = timer()
        try:
            frame = tello.get_frame_read().frame
        except Exception:
            print ('\nExit . . .\n')
            break
        end = timer()
        print("Elapsed Time on Thrad: " , end - start) 

if __name__ == "__main__":

    tello = initialize()
	
    #Thread Configuration
    frame = None
    frameThread = threading.Thread(target=frame_thread)
    frameThread.daemon = True
    frameThread.start()
	
    while True:
        time.sleep(1)

	
