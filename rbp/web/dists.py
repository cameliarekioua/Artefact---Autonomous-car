
import cv2
import cv2.aruco as aruco
import numpy as np

#REGRESSION

a =  13.3145
b = -0.9477

def get_dist(frame,aruco_dict,parameters):
#TODO : vérifier que la longueur est la bonne 
    aruco_marker_side_length = 0.0785
    x=0
    data = np.load('./camera_calibration.npz')
    mtx = data['mtx']
    dst = data['dist']
    dists = []
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers in the frame
    corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #if there are markers
    if len(corners) > 0:
        rvecs, tvecs, obj_points = cv2.aruco.estimatePoseSingleMarkers(corners,aruco_marker_side_length,mtx,dst) 
        for i in range(len(ids)):
            d = np.sqrt( tvecs[i][0][0]**2 + tvecs[i][0][1]**2 + tvecs[i][0][2]**2)
            real_d = a*d + b
            dists.append(real_d)
    return dists,ids
