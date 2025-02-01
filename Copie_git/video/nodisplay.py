
import cv2
import cv2.aruco as aruco

# Initialize the camera
cap = cv2.VideoCapture(0,cv2.CAP_V4L2)  # 0 for the default camera, or provide a video file path

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Define the ArUco dictionary (e.g., DICT_6X6_250) and parameters for the detector
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()
x=0
while True:
    # Read a frame from the video stream
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers in the frame
    corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If markers are detected, draw the markers and their IDs
    if len(corners) > 0:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        print(1)
        # Optionally, draw additional information (e.g., the IDs of the markers)
        for i in range(len(ids)):
            cv2.putText(frame, f"ID: {ids[i][0]}", 
                        (int(corners[i][0][0][0]), int(corners[i][0][0][1])), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
   # cv2.imshow('ArUco Marker Detection', frame)

    # Exit on pressing 'q'
    if x>100:
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
