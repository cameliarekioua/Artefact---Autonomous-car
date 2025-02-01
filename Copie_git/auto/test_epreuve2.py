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

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters_create()


from math import radians, cos, sin


def normalize_angle(angle):
    return angle % 360


def distance_to_ticks(distance_cm):
    circumference = WHELL_CIRCUMFERENCE
    revolutions_needed = distance_cm / circumference
    ticks_needed = revolutions_needed * TICKS_PER_REVOLUTION
    return int(ticks_needed)


def forward(c: controller.Controller, distance_cm: float, base_speed: int = 60):
    global position, direction

    ticks_to_move = distance_to_ticks(distance_cm)

    ticks_done_left = 0
    ticks_done_right = 0

    c.set_motor_speed(base_speed, base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move or ticks_done_right < ticks_to_move:
        left_ticks, right_ticks = c.get_encoder_ticks()

        ticks_done_left += left_ticks
        ticks_done_right += right_ticks

        tick_difference = ticks_done_left - ticks_done_right

        if abs(tick_difference) > 5:
            if tick_difference > 0:
                left_speed = max(0, base_speed - 5)
                right_speed = min(127, base_speed + 5)
            else:
                left_speed = min(127, base_speed + 5)
                right_speed = max(0, base_speed - 5)
        else:
            left_speed = base_speed
            right_speed = base_speed

        c.set_motor_speed(left_speed, right_speed)

        time.sleep(0.05)

    position[0] += distance_cm * cos(radians(direction))
    position[1] += distance_cm * sin(radians(direction))

    c.standby()
    time.sleep(0.1)


def backward(c: controller.Controller, distance_cm: float, base_speed: int = 60):
    global position, direction

    if distance_cm <= 0:
        raise ValueError("La distance doit être un nombre positif.")

    ticks_to_move = distance_to_ticks(distance_cm)

    ticks_done_left = 0
    ticks_done_right = 0

    c.set_motor_speed(-base_speed, -base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move or ticks_done_right < ticks_to_move:
        left_ticks, right_ticks = c.get_encoder_ticks()

        ticks_done_left += abs(left_ticks)
        ticks_done_right += abs(right_ticks)

        tick_difference = ticks_done_left - ticks_done_right
        if abs(tick_difference) > 5:
            adjustment = -1 * int(tick_difference / 10)
            left_speed = (
                -base_speed - adjustment if tick_difference > 0 else -base_speed
            )
            right_speed = (
                -base_speed + adjustment if tick_difference < 0 else -base_speed
            )
            left_speed = max(-127, min(0, left_speed))
            right_speed = max(-127, min(0, right_speed))
            c.set_motor_speed(left_speed, right_speed)
        else:
            c.set_motor_speed(-base_speed, -base_speed)

        time.sleep(0.05)

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

    c.set_motor_speed(-base_speed, base_speed)

    time.sleep(0.1)

    while ticks_done_left < ticks_to_move and ticks_done_right < ticks_to_move:
        left, right = c.get_encoder_ticks()
        ticks_done_left += abs(left)
        ticks_done_right += abs(right)

        tick_difference = ticks_done_left - ticks_done_right
        if abs(tick_difference) > 5:
            adjustment = tick_difference // 10
            left_speed = base_speed - adjustment if tick_difference > 0 else base_speed
            right_speed = base_speed + adjustment if tick_difference < 0 else base_speed

            left_speed = max(0, min(127, left_speed))
            right_speed = max(0, min(127, right_speed))

            c.set_motor_speed(-left_speed, right_speed)
        else:
            c.set_motor_speed(-base_speed, base_speed)

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

    c.set_motor_speed(base_speed, -base_speed)
    time.sleep(0.1)

    while ticks_done_left < ticks_to_move and ticks_done_right < ticks_to_move:
        left, right = c.get_encoder_ticks()
        ticks_done_left += abs(left)
        ticks_done_right += abs(right)

        tick_difference = ticks_done_left - ticks_done_right
        if abs(tick_difference) > 5:
            adjustment = tick_difference // 10
            left_speed = base_speed - adjustment if tick_difference > 0 else base_speed
            right_speed = base_speed + adjustment if tick_difference < 0 else base_speed

            left_speed = max(0, min(127, left_speed))
            right_speed = max(0, min(127, right_speed))

            c.set_motor_speed(left_speed, -right_speed)
        else:
            c.set_motor_speed(base_speed, -base_speed)

        time.sleep(0.05)

    direction = normalize_angle(direction - angle)

    c.standby()
    time.sleep(0.1)


speed = 30


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


def try_balise(found, balise, prev, frame):
    new_prev = False
    dists, corners, ids, rejected_img_points = detecte_balise(
        frame, aruco_dict, parameters
    )
    for i in range(len(ids) if ids else 0):
        if ids[i] in balise and dists[i] < 50:
            found.append(ids[i])
            balise.remove(ids[i])
        if ids[i] == 0:
            new_prev = True
    return found, balise, prev


def detecte(c, found, balise, prev, frame):
    new_prev = False
    print("a")
    time.sleep(1)
    turn_right(c, 45, speed)
    print("b")
    found, balise, nprev = try_balise(found, balise, prev, frame)
    new_prev = new_prev or nprev
    turn_left(c, 90, speed)
    found, balise, nprev = try_balise(found, balise, prev, frame)
    new_prev = nprev or new_prev
    turn_right(c, 45, speed)
    if prev:
        turn_left(c, 135, speed)
        found, balise, nprev = try_balise(found, balise, prev, frame)
        new_prev = nprev or new_prev
        turn_left(c, 90, speed)
        found, balise, nprev = try_balise(found, balise, prev, frame)
        new_prev = nprev or new_prev
        turn_left(c, 135, speed)
    return found, balise, new_prev


def capture_the_flag(c: controller.Controller):
    found = []
    turn_right(c, 30, speed)
    balise = [i for i in range(5, 17)]
    cols = 3
    rows = 7
    prev = True
    x = 0
    y = 0
    while y < rows - 1:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        found, balise, prev = detecte(c, found, balise, prev, frame)
        y += 1
        forward(c, 50, speed)
    turn_right(c, 90, speed)
    forward(c, 50, speed)
    x += 1
    turn_right(c, 90, speed)
    while y > 0:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        found, balise, prev = detecte(c, found, balise, prev, frame)
        y += 1
        forward(c, 50, speed)
    turn_left(c, 90, speed)
    forward(c, 50, speed)
    x += 1
    turn_left(c, 50, speed)
    while y < rows - 1:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        found, balise, prev = detecte(c, found, balise, prev, frame)
        y += 1
        forward(c, 50, speed)


def capture():
    c = controller.Controller()
    turn_right()


"""
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
"""


def test_epreuve2():
    c = controller.Controller()
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        exit()

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
    parameters = aruco.DetectorParameters_create()
    for _ in range(3):
        # capture d'une frame
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
        dist, ids, corner, detected_image_points = detecte_balise(
            frame, aruco_dict, parameters
        )
        if len(ids) > 0:
            print(1)
        # avancer
        forward(c, 50, 10)


def request_position():
    while running:
        print(position)
        time.sleep(1)


# Envoyé une requete pour mettre le robot sur sa position initiale
c = controller.Controller()
