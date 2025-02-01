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
    time.sleep(0.5)


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

        time.sleep(0.5)

    position[0] -= distance_cm * cos(radians(direction))
    position[1] -= distance_cm * sin(radians(direction))

    c.standby()
    time.sleep(0.1)


def turn_left(c: controller.Controller, angle: float, base_speed: int = 60):
    global direction

    if not (0 < base_speed <= 127):
        raise ValueError("La vitesse de base doit être entre 0 et 127.")

    robot_width_cm = 20.1
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

        time.sleep(0.5)

    direction = normalize_angle(direction + angle)

    c.standby()
    time.sleep(0.5)


def turn_right(c: controller.Controller, angle: float, base_speed: int = 60):
    global direction

    
    if not (0 < base_speed <= 127):
        raise ValueError("La vitesse de base doit être entre 0 et 127.")

    robot_width_cm = 20.1
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
    time.sleep(0.5)


speed = 20


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




c = controller.Controller()
running = True


def do_360():
    turn_right(c, 350, 10)
    running = False


t = threading.Thread(target=do_360)
t.start()


t.join()

