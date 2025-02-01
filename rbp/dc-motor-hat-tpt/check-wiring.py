#! /usr/bin/env python3

import controller
import time


def check_move(c: controller.Controller, left: bool):
    side, other_side, idx, oidx = "left", "right", 0, 1
    if not left:
        side, other_side, idx, oidx = other_side, side, oidx, idx
    c.standby()
    c.get_encoder_ticks()
    print(f"Making {side} motor go forward")
    speed = [110, 127]
    c.set_raw_motor_speed(*speed)
    time.sleep(2.0)
    c.standby()
    time.sleep(0.1)
    ticks = list(c.get_encoder_ticks())
    print(ticks)
    ticks, parasitic = ticks[idx], ticks[oidx]
    


def check_procedure():
    print(
        "Wheels will move forward (left then right), and encoder values will be checked"
    )
    c = controller.Controller()
    c.set_motor_shutdown_timeout(2)
    c.standby()
    time.sleep(0.1)
    check_move(c, True)
    time.sleep(2.0)
    check_move(c, False)


if __name__ == "__main__":
    try:
        check_procedure()
        print(
            "If you saw the wheels move forward as expected (left, then right), "
            + "everything is fine"
        )
    except ValueError as v:
        print(f"ERROR: {v}")
        print("Check that motors and encoders are correctly wired")
