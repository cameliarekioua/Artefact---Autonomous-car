import controller
import time
import sys

WHELL_CIRCUMFERENCE = 20.7
WHEEL_DIAMETER_CM = 6.0
TICKS_PER_REVOLUTION = 120 * 32


def distance_to_ticks(distance_cm):
    circumference = WHELL_CIRCUMFERENCE
    revolutions_needed = distance_cm / circumference
    ticks_needed = revolutions_needed * TICKS_PER_REVOLUTION
    return int(ticks_needed)
def normalize_angle(angle):
    return angle % 360

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
        time.sleep(0.005)

    # Mettre à jour la position
  

    c.standby()
    time.sleep(0.1)


def turn_left(c: controller.Controller, angle: float, base_speed: int = 60):

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

    c.standby()
    time.sleep(0.1)


def turn_right(c: controller.Controller, angle: float, base_speed: int = 60):

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

    c.standby()
    time.sleep(0.1)


def backward(c: controller.Controller, distance_cm: float, base_speed: int = 60):

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
        if abs(tick_difference) > 5:  # Si l'écart est supérieur à un seuil
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

    c.standby()
    time.sleep(0.1)


if __name__ == "__main__":
    try:
        c = controller.Controller()
        match sys.argv[1]:
            case "forward":
                distance = float(sys.argv[2])
                base_speed = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                forward(c, distance, base_speed)
            case "turn_right":
                angle = float(sys.argv[2])
                base_speed = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                turn_right(c, angle, base_speed)
            case "backward":
                distance = float(sys.argv[2])
                base_speed = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                backward(c, distance, base_speed)
            case "turn_left":
                angle = float(sys.argv[2])
                base_speed = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                turn_left(c, angle, base_speed)
            case _:
                print("This arg is not accepted")
    except ValueError as v:
        print(f"ERROR: {v}")
        print("Check that motors and encoders are correctly wired")
    except IndexError:
        print(
            "ERROR: Please provide a distance in centimeters and optionally a base speed."
        )
