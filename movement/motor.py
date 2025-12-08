from RPi.GPIO import *
from .pin_definition import *

is_initialized = False
pwm_l: PWM
pwm_r: PWM

def init():
    # setup pins
    setup(EN_L, OUT, initial=HIGH)
    setup(EN_R, OUT, initial=HIGH)
    setup(IN_LB, OUT, initial=LOW)
    setup(IN_LF, OUT, initial=LOW)
    setup(IN_RB, OUT, initial=LOW)
    setup(IN_RF, OUT, initial=LOW)
    # setup PWM
    global is_initialized
    global pwm_l
    global pwm_r
    pwm_freq = 50
    pwm_l = PWM(EN_L, pwm_freq)
    pwm_l.start(100)
    pwm_r = PWM(EN_R, pwm_freq)
    pwm_r.start(100)
    is_initialized = True

def check_init():
    if not is_initialized:
        print("Initializing motor GPIO...")
        print("If you don't want to see this message, please invoke 'init()' before using other functions.")
        init()

def stop():
    check_init()
    output(IN_LB, LOW)
    output(IN_LF, LOW)
    output(IN_RB, LOW)
    output(IN_RF, LOW)

def release():
    if not is_initialized:
        return
    global is_initialized
    is_initialized = False
    stop()
    pwm_l.stop()
    pwm_r.stop()

def forward():
    check_init()
    output(IN_LF, HIGH)
    output(IN_RF, HIGH)
    output(IN_LB, LOW)
    output(IN_RB, LOW)

def backward():
    check_init()
    output(IN_LF, LOW)
    output(IN_RF, LOW)
    output(IN_LB, HIGH)
    output(IN_RB, HIGH)

def turn_left():
    check_init()
    output(IN_LF, HIGH)
    output(IN_RF, LOW)
    output(IN_LB, LOW)
    output(IN_RB, HIGH)

def turn_right():
    check_init()
    output(IN_LF, LOW)
    output(IN_RF, HIGH)
    output(IN_LB, HIGH)
    output(IN_RB, LOW)

def speed_left(c: float):
    check_init()
    pwm_l.ChangeDutyCycle(c)

def speed_right(c: float):
    check_init()
    pwm_r.ChangeDutyCycle(c)

__all__ = [
    'init', 'stop', 'release',
    'forward', 'backward', 'turn_left', 'turn_right',
    'speed_left', 'speed_right',
]
