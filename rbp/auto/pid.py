import controller
import time
import threading
import cv2
import cv2.aruco as aruco
import numpy as np
from dists import get_dist
WHELL_CIRCUMFERENCE = 21.3
WHEEL_DIAMETER_CM = 6.0
TICKS_PER_REVOLUTION = 120 * 32

position = [25, 25]
direction = 0
running = True

from math import radians, cos, sin


def normalize_angle(angle):
    return angle % 360


def distance_to_ticks(distance_cm):
    circumference = WHELL_CIRCUMFERENCE
    revolutions_needed = distance_cm / circumference
    ticks_needed = revolutions_needed * TICKS_PER_REVOLUTION
    return int(ticks_needed)


class PID:
    def __init__(self, kp, ki, kd):
        # Coefficients PID
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # Variables pour l'intégrale et la dérivée
        self.prev_error = 0
        self.integral = 0

    def update(self, error):
        """ Calcule la sortie PID basée sur l'erreur. """
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        # Calcul de la sortie PID
        return int (self.kp * error + self.ki * self.integral + self.kd * derivative)




def forward(c: controller.Controller, distance_cm: float, base_speed: int = 20):
    global position, direction

    ticks_to_move = distance_to_ticks(distance_cm)
    ticks_done_left = 0
    ticks_done_right = 0

    # Initialisation du PID
    pid = PID(kp=1.0, ki=0.1, kd=0.05)

    c.set_motor_speed(base_speed, base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move or ticks_done_right < ticks_to_move:
        left_ticks, right_ticks = c.get_encoder_ticks()

        ticks_done_left += left_ticks
        ticks_done_right += right_ticks

        # Calculer l'erreur entre les ticks des deux roues
        error = ticks_done_left - ticks_done_right
        adjustment = pid.update(error)  # Utilisation du PID pour ajuster l'erreur

        # Calculer la vitesse des moteurs avec l'ajustement du PID
        left_speed = base_speed + adjustment
        right_speed = base_speed - adjustment

        # Limiter la vitesse pour éviter des dépassements
        left_speed = max(0, min(127, left_speed))
        right_speed = max(0, min(127, right_speed))
        c.set_motor_speed(left_speed, right_speed)
        time.sleep(0.05)

    # Mettre à jour la position
    position[0] += distance_cm * cos(radians(direction))
    position[1] += distance_cm * sin(radians(direction))

    c.standby()
    time.sleep(0.1)



def backward(c: controller.Controller, distance_cm: float, base_speed: int = 20):
    global position, direction

    if distance_cm <= 0:
        raise ValueError("La distance doit être un nombre positif.")

    ticks_to_move = distance_to_ticks(distance_cm)
    ticks_done_left = 0
    ticks_done_right = 0

    # Initialisation du PID
    pid = PID(kp=1.0, ki=0.1, kd=0.05)

    c.set_motor_speed(-base_speed, -base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move or ticks_done_right < ticks_to_move:
        left_ticks, right_ticks = c.get_encoder_ticks()

        ticks_done_left += abs(left_ticks)
        ticks_done_right += abs(right_ticks)

        # Calculer l'erreur
        error = ticks_done_left - ticks_done_right
        adjustment = pid.update(error)  # Utilisation du PID pour ajuster l'erreur

        # Calculer la vitesse des moteurs avec l'ajustement du PID
        left_speed = -base_speed - adjustment
        right_speed = -base_speed + adjustment

        # Limiter la vitesse pour éviter des dépassements
        left_speed = max(-127, min(0, left_speed))
        right_speed = max(-127, min(0, right_speed))

        c.set_motor_speed(left_speed, right_speed)
        time.sleep(0.05)

    # Mettre à jour la position
    position[0] -= distance_cm * cos(radians(direction))
    position[1] -= distance_cm * sin(radians(direction))

    c.standby()
    time.sleep(0.1)




def turn_left(c: controller.Controller, angle: float, base_speed: int = 60):
    global direction

    if not (0 < base_speed <= 127):
        raise ValueError("La vitesse de base doit être entre 0 et 127.")

    robot_width_cm = 19.8
    wheel_circumference = 21.3

    arc_length = (3.14159 * robot_width_cm * angle) / 360
    ticks_to_move = distance_to_ticks(arc_length)

    ticks_done_left = 0
    ticks_done_right = 0

    # Initialisation du PID
    pid = PID(kp=0.43, ki=0.01, kd=0.01)

    c.set_motor_speed(-base_speed, base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move and ticks_done_right < ticks_to_move:
        left, right = c.get_encoder_ticks()
        ticks_done_left += abs(left)
        ticks_done_right += abs(right)

        # Calculer l'erreur entre les deux roues
        error = ticks_done_left - ticks_done_right
        adjustment = pid.update(error)  # Utilisation du PID pour ajuster l'erreur

        # Calculer la vitesse des moteurs avec l'ajustement du PID
        left_speed = base_speed - adjustment
        right_speed = base_speed + adjustment

        # Limiter la vitesse pour éviter des dépassements
        left_speed = max(0, min(127, left_speed))
        right_speed = max(0, min(127, right_speed))

        c.set_motor_speed(-left_speed, right_speed)
        time.sleep(0.05)

    direction = normalize_angle(direction + angle)

    c.standby()
    time.sleep(0.1)


def turn_right(c: controller.Controller, angle: float, base_speed: int = 60):
    global direction

    if not (0 < angle <= 360):
        raise ValueError("L'angle doit être compris entre 0 et 360 degrés.")
    if not (0 < base_speed <= 127):
        raise ValueError("La vitesse de base doit être entre 0 et 127.")

    robot_width_cm = 19.8
    wheel_circumference = 21.3

    arc_length = (3.14159 * robot_width_cm * angle) / 360
    ticks_to_move = distance_to_ticks(arc_length)

    ticks_done_left = 0
    ticks_done_right = 0

    # Initialisation du PID
    pid = PID(kp=1.0, ki=0.1, kd=0.05)

    c.set_motor_speed(base_speed, -base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move and ticks_done_right < ticks_to_move:
        left, right = c.get_encoder_ticks()
        ticks_done_left += abs(left)
        ticks_done_right += abs(right)

        # Calculer l'erreur entre les deux roues
        error = ticks_done_left - ticks_done_right
        adjustment = pid.update(error)  # Utilisation du PID pour ajuster l'erreur

        # Calculer la vitesse des moteurs avec l'ajustement du PID
        left_speed = base_speed - adjustment
        right_speed = base_speed + adjustment

        # Limiter la vitesse pour éviter des dépassements
        left_speed = max(0, min(127, left_speed))
        right_speed = max(0, min(127, right_speed))

        c.set_motor_speed(left_speed, -right_speed)
        time.sleep(0.05)

    direction = normalize_angle(direction - angle)

    c.standby()
    time.sleep(0.1)

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
            d = np.sqrt(tvecs[i][0][0] ** 2 + tvecs[i][0][1] ** 2 + tvecs[i][0][2] ** 2)
            real_d = a * d + b
            dists.append(real_d)
    return dists, corners, ids, rejected_img_points


def capture_the_flag(c: controller.Controller):
    found = []
    balise = [i for i in range(5, 17)]  # les balises que l'on veut trouver
    dimension = 6
    cell_position = [0, 0]
    # VIDEO
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        exit()

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
    parameters = aruco.DetectorParameters_create()

    while len(found) < 2:
        debut = 0
        while debut < dimension:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image")
                break
            dist, ids, corner, detected_image_points = detecte_balise(
                frame, aruco_dict, parameters
            )

            if len(corner) > 0 and dist < 50 and ids in balise:
                # requete à envoyer au serveur pour dire qu'on a trouvé une balise
                found.append(ids)
            cell_position[1] += 1
            forward(c, 50, speed)
            debut += 1
        turn_right(c, 180, speed)
        debut = 0
        while debut < dimension:
            dist, corner, ids, detected_image_points = detecte_balise()
            if len(corner) > 0 and dist < 50 and ids in balise:
                # requete à envoyer au serveur pour dire qu'on a trouvé une balise
                found.append(ids)
            forward(c, 50, speed)
            cell_position[1] -= 1
            debut += 1

        turn_left(c, 90, speed)
        forward(c, 50, speed)
        cell_position[0] += 1
        turn_left(c, 90, speed)
        # on boucle si pas trouvé
        if cell_position[0] == dimension + 1:
            turn_left(c, 90, speed)
            forward(c, (dimension + 1) * 50, speed)
            turn_right(c, 90, speed)
def test_epreuve2():
    c = controller.Controller()
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        exit()

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
    parameters = aruco.DetectorParameters_create()
    forward(c,25,10)
    turn_left(c,45,15)
    turn_right(c,90,15)
    turn_left(c,45,15)
    forward(c,25,10)

test_epreuve2()
