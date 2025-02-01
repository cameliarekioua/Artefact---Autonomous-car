import controller
import time
import threading
import cv2
import cv2.aruco as aruco
import numpy as np
import subprocess
from newpid import forward
from dists import get_dist
WHELL_CIRCUMFERENCE = 21.3
WHEEL_DIAMETER_CM = 6.0
TICKS_PER_REVOLUTION = 120 * 32

position = [25, -25]
direction = 0
running = True
running2 = True


from math import radians, cos, sin


def normalize_angle(angle):
    return angle % 360


def distance_to_ticks(distance_cm):
    circumference = WHELL_CIRCUMFERENCE
    revolutions_needed = distance_cm / circumference
    ticks_needed = revolutions_needed * TICKS_PER_REVOLUTION
    return int(ticks_needed)


def ticks_to_distance(ticks):
    circumference = WHELL_CIRCUMFERENCE
    return (ticks / TICKS_PER_REVOLUTION) * circumference

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
        error = abs(error)
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
    b_speed = base_speed
    # Initialisation du PID
    pid = PID(kp=0.5, ki=0.00001, kd=0.005)
    base_speed = 0
    c.set_motor_speed(base_speed, base_speed)  # Initialisation de la vitesse de base
#    time.sleep(0.1)

    while ticks_done_left < ticks_to_move or ticks_done_right < ticks_to_move:
        left_ticks, right_ticks = c.get_encoder_ticks()
        base_speed  = min (base_speed+1,b_speed)
        ticks_done_left += left_ticks
        ticks_done_right += right_ticks

        # Calculer l'erreur entre les ticks des deux roues
        error = ticks_done_left - ticks_done_right
        adjustment = pid.update(error)  # Utilisation du PID pour ajuster l'erreur

        # Appliquer l'ajustement en fonction du signe de l'erreur
        if error > 0:
            # Si l'erreur est positive, ralentir la roue gauche et accélérer la droite
            left_speed = base_speed - adjustment
            right_speed = base_speed + adjustment
        else:
            # Si l'erreur est négative, ralentir la roue droite et accélérer la gauche
            left_speed = base_speed + adjustment
            right_speed = base_speed - adjustment

        # Limiter la vitesse pour éviter des dépassements
        left_speed = max(0, min(b_speed+10, left_speed))
        right_speed = max(0, min(b_speed+10, right_speed))

        c.set_motor_speed(left_speed, right_speed)

        position[0] += ticks_to_distance((left_ticks + right_ticks) / 2) * sin(
            radians(direction)
        )
        position[1] += ticks_to_distance((left_ticks + right_ticks) / 2) * cos(
            radians(direction)
        )
        time.sleep(0.005)

    # Mettre à jour la position
    c.standby()
    time.sleep(0.1)


"""
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

        position[0] += ticks_to_distance((left_ticks + right_ticks) / 2) * sin(
            radians(direction)
        )
        position[1] += ticks_to_distance((left_ticks + right_ticks) / 2) * cos(
            radians(direction)
        )

        time.sleep(0.05)

    c.standby()
    time.sleep(0.1)
"""

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

        position[0] += ticks_to_distance((left_ticks + right_ticks) / 2) * sin(
            radians(direction)
        )
        position[1] += ticks_to_distance((left_ticks + right_ticks) / 2) * cos(
            radians(direction)
        )

        time.sleep(0.05)

    c.standby()
    time.sleep(0.1)


def turn_left(c: controller.Controller, angle: float, base_speed: int = 60):
    global direction

    if not (0 < base_speed <= 127):
        raise ValueError("La vitesse de base doit être entre 0 et 127.")

    robot_width_cm = 21
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

    direction = normalize_angle(direction - angle)

    c.standby()
    time.sleep(0.1)


def turn_right(c: controller.Controller, angle: float, base_speed: int = 60):
    global direction

    if not (0 < angle <= 360):
        raise ValueError("L'angle doit être compris entre 0 et 360 degrés.")
    if not (0 < base_speed <= 127):
        raise ValueError("La vitesse de base doit être entre 0 et 127.")

    robot_width_cm = 21
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

    direction = normalize_angle(direction + angle)

    c.standby()
    time.sleep(0.1)

def request_position():
    while running2:
        subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/api/pos?x=' + str(position[0]) + '&y=' + str(position[1])])
        print(position)  # a remplacer par la requete
        time.sleep(1)


request_thread = threading.Thread(target=request_position)

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
            d = np.sqrt(tvecs[i][0][0] ** 2 + tvecs[i][0][1] ** 2 + tvecs[i][0][2] ** 2)
            real_d = a * d + b
            dists.append(real_d)
    return dists, corners, ids, rejected_img_points


# VIDEO
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters_create()

c = controller.Controller()
running = False


def find_balise(found, balise, x, y):
    global running
    running = True

    def do_360():
        global running
        turn_right(c, 360, 12)
        running = False

    t = threading.Thread(target=do_360)
    t.start()
    while running:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        dists,  ids = get_dist(
            frame, aruco_dict, parameters
        )
        if ids is not None:
            for i in range(len(ids)):
                print(ids[i], dists[i])
                if ids[i] in balise and dists[i] < 50:
                    x = position
                    print(1)
                    subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/api/marker?id=' + str(ids[i]) + '&col=' + str(x*50) + '&row=' + str(y*50 - 50)])
                    found = found + 1
                    balise.remove(ids[i])
                    break
    t.join()
    return found, balise


from math import atan2, degrees, sqrt


def move_to_position(
    c: controller.Controller, start_pos: tuple, end_pos: tuple, base_speed: int = 20
):
    global position, direction

    x_start, y_start = start_pos
    x_end, y_end = end_pos

    dx = x_end - x_start
    dy = y_end - y_start

    distance = sqrt(dx**2 + dy**2)

    target_angle = degrees(atan2(dx, dy))

    rotation_angle = target_angle - direction

    rotation_angle = normalize(rotation_angle)

    if rotation_angle > 0:
        turn_right(c, rotation_angle, base_speed)
    else:
        turn_left(c, -rotation_angle, base_speed)

    forward(c, distance, base_speed)

    position = (x_end, y_end)
    direction = target_angle


def normalize(angle: float) -> float:

    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def capture_the_flag(c: controller.Controller):

    running2 = True
    running = True
    request_thread.start()
    found = 0
    balise = [i for i in range(5, 17)]
    cols = 3
    rows = 7
    prev = True
    x = 0
    y = 0
    last_correction = 0
    while y < rows - 1:
        found, balise = find_balise(found, balise, x, y)
        y += 1
        forward(c, 50, speed)
        last_correction += 1

        if last_correction >= 2:
            # correct_position(c, target_direction=0)
            last_correction = 0
    turn_right(c, 90, speed)
    forward(c, 50, speed)
    x += 1
    turn_right(c, 90, speed)
    last_correction += 1
    while y > 0:
        found, balise = find_balise(found, balise, x, y)
        y += 1
        forward(c, 50, speed)
        last_correction += 1

        if last_correction >= 2:
            # correct_position(c, target_direction=180)
            last_correction = 0

    turn_left(c, 90, speed)
    forward(c, 50, speed)
    x += 1
    turn_left(c, 50, speed)
    last_correction += 1

    while y < rows - 1:
        found, balise = find_balise(found, balise, x, y)
        y += 1
        forward(c, 50, speed)
        last_correction += 1

        if last_correction >= 2:
            # correct_position(c, target_direction=0)
            last_correction = 0
    running = False
    running2 = False
    request_thread.join()
    cap.release()
    cv2.destroyAllWindows()

def correct_position(c: controller.Controller, target_direction: float):

    global position, direction

    theoretical_position = triangulize()

    print(f"Correction: déplacement vers la position théorique {theoretical_position}")
    move_to_position(c, position, theoretical_position, speed)

    position = theoretical_position

    angle_to_turn = normalize_angle(target_direction - direction)
    if angle_to_turn > 0:
        turn_right(c, angle_to_turn, speed)
    elif angle_to_turn < 0:
        turn_left(c, -angle_to_turn, speed)

    direction = target_direction
for i in range(3):
    turn_right(c, 360 - 40/3, 10)
    time.sleep(1)


