# on veut aller de x,y à z,w
# (0,0) en bas a gauche
import controller
import time
import threading
import subprocess
import cv2
import cv2.aruco as aruco
import numpy as np
from dists import get_dist

WHELL_CIRCUMFERENCE = 20.7
WHEEL_DIAMETER_CM = 6.0
TICKS_PER_REVOLUTION = 120 * 32

position = [25, -25]
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

    robot_width_cm = 19.3
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

    robot_width_cm = 19.3
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
    while running:
        print(position)  # a remplacer par la requete
        subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/pos?x=' + str(position[0]) + '&y=' + str(position[1])])
        time.sleep(1)


request_thread = threading.Thread(target=request_position)

subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/pos?x=25&y=-25'])

def move_1(src, to):

    # subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/api/start'])

    request_thread.start()

    c = controller.Controller()

    def move(src, to):
        x, y = src
        x1, y1 = to
        speed = 10
        dx = x1 - x
        dy = y1 - y
        # on va a gauche

        forward(c, dy * 50, speed)
        if dx < 0:
            # aller a gacuhe de |dx| cases
            turn_left(c, 90, speed)
            dx = -dx
            forward(c, 50 * dx, speed)
        else:
            # aller a droite de dx cases
            turn_right(c, 90, speed)
            forward(c, 50 * dx, speed)
        turn_right(c, 350, speed)

        col = str(int(position[0] // 50) + 1)
        y = int(position[1] // 50) + 1
        print('col = '+ col)
        print('y = ' + str(y))
        row = "G" if y==0 else ("F" if y==1 else ("E" if y==2 else ("D" if y==3 else ("C" if y==4 else ("B" if y==5 else ("A" if y==6 else ""))))))
        subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/marker?id=5&col=' + col + '&row=' + row])
        print('http://proj103.r2.enst.fr/marker?id=5&col=' + col + '&row=' + row)
        # penser à envoyer au serveur caputre de drapeau 5 + position
        print("arrivé")

    try:
        move(src, to)
    finally:
        global running
        running = False
        request_thread.join()
        # subprocess.run(["curl", "-X", "POST", 'http://proj103.r2.enst.fr/api/stop'])

