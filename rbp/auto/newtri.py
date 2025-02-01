import controller
import time
import threading
import cv2
import cv2.aruco as aruco
import numpy as np


WHELL_CIRCUMFERENCE = 21.3
WHEEL_DIAMETER_CM = 6.0
TICKS_PER_REVOLUTION = 120 * 32

position = [25, 25]
direction = 0
running = True


from math import radians, cos, sin


def detecte_balise(frame, aruco_dict, parameters):
    a = 13.3145
    b = -0.9477
    # TODO : vérifier que la longueur est la bonne
    aruco_marker_side_length = 2
    x = 0
    data = np.load("./camera_calibration.npz")
    mtx = data["mtx"]
    dst = data["dist"]
    dists = []
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers in the frame
    corners, ids, rejected_img_points = aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
    )
    # if there are markers
    if len(corners) > 0:
        rvecs, tvecs, obj_points = cv2.aruco.estimatePoseSingleMarkers(
            corners, aruco_marker_side_length, mtx, dst
        )
        for i in range(len(ids)):
            if ids[i] in big_bals:
                _,tv,_ = cv2.aruco.estimatePoseSingleMarkers(corners, 10, mtx, dst)
                t1 =  tv[i][0][1]
                t2 = tv[i][0][2]
                t0 =  tv[i][0][0]
            else:
                t1 =  tvecs[i][0][1]
                t2 = tvecs[i][0][2]
                t0 =  tvecs[i][0][0]
            d = np.sqrt(t0 ** 2 + t1 ** 2 + t2 ** 2)
            real_d = a * d + b
            dists.append(real_d)
    return dists, corners, ids, rejected_img_points



