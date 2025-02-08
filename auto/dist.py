from dists import get_dist
import cv2
import cv2.aruco as aruco




# Initialize the camera
cap = cv2.VideoCapture(0,cv2.CAP_V4L2)  # 0 for the default camera, or provide a video file path

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Define the ArUco dictionary (e.g., DICT_6X6_250) and parameters for the detector
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters_create()
#TODO : vérifier que la longueur est la bonne EN CM 
aruco_marker_side_length = 2
x=0



while True:
    # Read a frame from the video stream
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    dists = get_dist(frame,aruco_dict,parameters)
    print(dists)
    if len(dists) > 0:
        print(1) 
    if x>100:
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
