from RPi.GPIO import *
from .pin_definition import *

def motor_init():
    setup(EN_A, OUT, initial=HIGH)
    setup(EN_B, OUT, initial=HIGH)
    setup(IN_LB, OUT, initial=LOW)
    setup(IN_LF, OUT, initial=LOW)
    setup(IN_RB, OUT, initial=LOW)
    setup(IN_RF, OUT, initial=LOW)

def motor_stop():
    output(IN_LB, LOW)
    output(IN_LF, LOW)
    output(IN_RB, LOW)
    output(IN_RF, LOW)

def motor_forward():
    output(IN_LF, HIGH)
    output(IN_RF, HIGH)
    output(IN_LB, LOW)
    output(IN_RB, LOW)

def motor_backward():
    output(IN_LF, LOW)
    output(IN_RF, LOW)
    output(IN_LB, HIGH)
    output(IN_RB, HIGH)

__all__ = [
    'motor_init',
    'motor_stop', 'motor_forward', 'motor_backward'
]
