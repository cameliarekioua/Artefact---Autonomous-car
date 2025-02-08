from math import atan2, degrees, sqrt

def move_to_position(c: controller.Controller, start_pos: tuple, end_pos: tuple, base_speed: int = 20):
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
    found = []
    turn_right(c, 30, speed)
    balise = [i for i in range(5, 17)]
    cols = 3
    rows = 7
    prev = True
    x = 0
    y = 0
    last_correction= 0 
    while y < rows - 1:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        found, balise, prev = detecte(c, found, balise, prev, frame)
        y += 1
        forward(c, 50, speed)
        last_correction+=1 

        if last_correction>=2 :
            correct_position(c,target_direction=0)
            last_correction = 0
    turn_right(c, 90, speed)
    forward(c, 50, speed)
    x += 1
    turn_right(c, 90, speed)
    last_correction+=1
    while y > 0:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        found, balise, prev = detecte(c, found, balise, prev, frame)
        y += 1
        forward(c, 50, speed)
        last_correction+=1

        if last_correction>=2 :
            correct_position(c,target_direction=180)
            last_correction = 0

    turn_left(c, 90, speed)
    forward(c, 50, speed)
    x += 1
    turn_left(c, 50, speed)
    last_correction+=1

    while y < rows - 1:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        found, balise, prev = detecte(c, found, balise, prev, frame)
        y += 1
        forward(c, 50, speed)
        last_correction+=1

        if last_correction>=2 :
            correct_position(c,target_direction=0)
            last_correction = 0

def correct_position(c: controller.Controller, target_direction: float):
   
    global position, direction

    theoretical_position = triangulize()

    print(f"Correction: déplacement vers la position théorique {theoretical_position}")
    move_to_position(c, position, theoretical_position, speed)


    position = theoretical_position

   
    angle_to_turn = normalize(target_direction - direction)
    if angle_to_turn > 0:
        turn_right(c, angle_to_turn, speed)
    elif angle_to_turn < 0:
        turn_left(c, -angle_to_turn, speed)


    direction = target_direction
