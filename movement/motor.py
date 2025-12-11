from .gpio import *

is_initialized = False
pwm_l: PWM
pwm_r: PWM

def init():
    global is_initialized
    global pwm_l
    global pwm_r
    # setup pins
    setup(EN_L, OUT, initial=HIGH)
    setup(EN_R, OUT, initial=HIGH)
    setup(IN_LB, OUT, initial=LOW)
    setup(IN_LF, OUT, initial=LOW)
    setup(IN_RB, OUT, initial=LOW)
    setup(IN_RF, OUT, initial=LOW)
    # setup PWM
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
    set(IN_LB, LOW)
    set(IN_LF, LOW)
    set(IN_RB, LOW)
    set(IN_RF, LOW)

def release():
    global is_initialized
    if not is_initialized:
        return
    stop()
    pwm_l.stop()
    pwm_r.stop()
    is_initialized = False

def forward():
    check_init()
    set(IN_LF, HIGH)
    set(IN_RF, HIGH)
    set(IN_LB, LOW)
    set(IN_RB, LOW)

def backward():
    check_init()
    set(IN_LF, LOW)
    set(IN_RF, LOW)
    set(IN_LB, HIGH)
    set(IN_RB, HIGH)

def turn_left():
    check_init()
    set(IN_LF, HIGH)
    set(IN_RF, LOW)
    set(IN_LB, LOW)
    set(IN_RB, HIGH)

def turn_right():
    check_init()
    set(IN_LF, LOW)
    set(IN_RF, HIGH)
    set(IN_LB, HIGH)
    set(IN_RB, LOW)

def speed_left(c: float):
    check_init()
    pwm_l.ChangeDutyCycle(c)

def speed_right(c: float):
    check_init()
    pwm_r.ChangeDutyCycle(c)

def map(x: float, y: float):
    """
    Map x, y coordinates to motor movements.
    x: -1 (left) to 1 (right)
    y: -1 (forward) to 1 (backward)
    """
    if x == 0 and y == 0:
        stop()
        return
    # set speeds
    base_speed = 100 * max(abs(x), abs(y))
    speed_left(base_speed * min(1, 1 + x))
    speed_right(base_speed * min(1, 1 - x))
    # start motor
    if y <= 0:  # forward
        forward()
    else:  # backward
        backward()

__all__ = [
    'init', 'stop', 'release', 'map',
    'forward', 'backward', 'turn_left', 'turn_right',
    'speed_left', 'speed_right',
]
