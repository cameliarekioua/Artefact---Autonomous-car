Content of the package
======================


## `controller.py`

This file contains a Python module used to interact with the embedded
firmware, for example to set the motor speed, or read the encoders.
Its version must match the one of the embedded firmware.

## `check-wiring.py`

This program checks that the motors are connected as expected by
moving them in turn. Also, it checks that the encoders receive the
right information and appear to be connected correctly.

