import controller
import time
import threading
import cv2
import cv2.aruco as aruco
import numpy as np
import math
from bouge import turn_right
WHELL_CIRCUMFERENCE = 21.3
WHEEL_DIAMETER_CM = 6.0
TICKS_PER_REVOLUTION = 120 * 32
position = [25, 25]
direction = 0
running = True

from math import radians, cos, sin
big_bals = [1,2,3,4]

c = controller.Controller()

def detecte_balise(frame, aruco_dict, parameters,aruco_size):
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


print("hehé")
def calculer_coordonnees_A(x_B, y_B, d_AB, theta_B_deg, x_C, y_C, d_AC, theta_C_deg):
    """
    Calcule les coordonnées du point A, sachant les coordonnées de B et C,
    les distances d_AB et d_AC, et les directions theta_B et theta_C par rapport à A.
    
    Args:
        x_B, y_B : coordonnées du point B.
        d_AB : distance entre A et B.
        theta_B_deg : direction de B par rapport à A en degrés (azimut).
        x_C, y_C : coordonnées du point C.
        d_AC : distance entre A et C.
        theta_C_deg : direction de C par rapport à A en degrés (azimut).
        
    Returns:
        (x_A, y_A) : coordonnées du point A.
    """
    # Conversion des directions de degrés en radians
    theta_B = math.radians(theta_B_deg)
    theta_C = math.radians(theta_C_deg)
    
    # Calcul des coordonnées de A en utilisant les équations ci-dessus
    x_A = (x_B - d_AB * math.cos(theta_B) + x_C - d_AC * math.cos(theta_C)) / 2
    y_A = (y_B - d_AB * math.sin(theta_B) + y_C - d_AC * math.sin(theta_C)) / 2
    
    return x_A, y_A

cap = cv2.VideoCapture(0,cv2.CAP_V4L2)
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters_create()
print("hah")
def where(up):
# VIDEO
    print("avant")
    h = get_dir(aruco_dict,parameters)
    # on suppose que 1 et 2 sont tjrs visibles
    x1,y1 = 0,6*50
    x2,y2 = 150,6*50 
    d1,alpha1 = h[1]
    d2,alpha2 = h[2]
    x3,y3 = 150,0
    x4,y4 = 0,0 
    d3,alpha3 = h[3]
    d4,alpha4 = h[4]
    if up:
        x_B  = x1
        y_B = y1
        alphaB = alpha1 
        x_C  = x2
        y_C = y2
        alphaC = alpha2
    else:
        x_B  = x3
        y_B = y3
        alphaB = alpha3 
        x_C  = x4
        y_C = y4
        alphaC = alpha4

    x,y = calculer_coordonnees_A(x_A, y_B, d1, np.pi/2-alphaB, x_C, y_C, d2, np.pi/2-alphaC)
    return x,y

def get_dir(aruco_dict,parameters):
    pas = 22.5
    dir =0 
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    ret, frame = cap.read()
    aruco_size = 10
    if not ret:
        print("Error: Failed to capture image")
    dic  = {}
    while dir < 360:
        print(1)
        time.sleep(0.5)
        dists, corners, ids, rejected_img_points = detecte_balise(frame, aruco_dict, parameters,aruco_size )
        for i in range(len(ids) if ids!=None else 0):
            if ids[i] in big_bals:
                dic[ids[i]] = (dists[i],dir)
        turn_right(c,22.5,10)
        dir += pas
    return dic

where(True)

cap.release()
cv2.destroyAllWindows()

















