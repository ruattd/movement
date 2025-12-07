from RPi.GPIO import *
from .pin_definition import *

is_initialized = False
pwm_lf: PWM
pwm_lb: PWM
pwm_rf: PWM
pwm_rb: PWM

def init():
    # setup pins
    setup(EN_A, OUT, initial=HIGH)
    setup(EN_B, OUT, initial=HIGH)
    setup(IN_LB, OUT, initial=LOW)
    setup(IN_LF, OUT, initial=LOW)
    setup(IN_RB, OUT, initial=LOW)
    setup(IN_RF, OUT, initial=LOW)
    # setup PWM
    global is_initialized
    global pwm_lf
    global pwm_lb
    global pwm_rf
    global pwm_rb
    pwm_freq = 2
    pwm_lf = PWM(IN_LF, pwm_freq)
    pwm_lf.start(100)
    pwm_lb = PWM(IN_LB, pwm_freq)
    pwm_lb.start(100)
    pwm_rf = PWM(IN_RF, pwm_freq)
    pwm_rf.start(100)
    pwm_rb = PWM(IN_RB, pwm_freq)
    pwm_rb.start(100)
    is_initialized = True

def check_init():
    if not is_initialized:
        print("Initializing motor GPIO...")
        print("If you don't want to see this message, please invoke 'init()' before using other functions.")

def stop():
    check_init()
    output(IN_LB, LOW)
    output(IN_LF, LOW)
    output(IN_RB, LOW)
    output(IN_RF, LOW)

def release():
    global is_initialized
    is_initialized = False
    stop()
    pwm_lf.stop()
    pwm_rf.stop()
    pwm_lb.stop()
    pwm_rb.stop()

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

def speed_left(c: int):
    pwm_lf.ChangeDutyCycle(c)
    pwm_lb.ChangeDutyCycle(c)

def speed_right(c: int):
    pwm_rf.ChangeDutyCycle(c)
    pwm_rb.ChangeDutyCycle(c)

__all__ = [
    'init', 'stop', 'release',
    'forward', 'backward', 'turn_left', 'turn_right',
    'speed_left', 'speed_right',
]
