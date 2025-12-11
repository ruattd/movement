from .gpio import *
import math

L = 0
M = 1
R = 2

is_initialized = False

pwm: list[PWM] = []

def init(enable_brightness: bool = False):
    global is_initialized
    rm = [LED0, LED1, LED2]
    for x in range(3):
        r = rm[x]
        setup(r, OUT, initial=HIGH)
        if enable_brightness:
            pwm.append(PWM(r, 200))
            pwm[x].start(0)
    is_initialized = True

def check_init(enable_brightness: bool = False):
    if not is_initialized:
        print("Initializing LED GPIO...")
        print("If you don't want to see this message, please invoke 'init()' before using other functions.")
        init(enable_brightness)

def remap(num: int):
    check_init()
    return [LED0, LED1, LED2][num]

def release():
    global is_initialized
    if not is_initialized:
        return
    rm = [LED0, LED1, LED2]
    for x in range(3):
        r = rm[x]
        if len(pwm):
            pwm[x].stop()
        set(r, HIGH)
        cleanup(r)
    is_initialized = False

def gamma(value: float, gamma: float = 2.2, max_val: float = 100.0) -> float:
    if value <= 0:
        return 0.0
    if value >= max_val:
        return max_val
    # Normalize input to 0.0 - 1.0
    normalized = value / max_val
    # Apply Power Law (Gamma Correction)
    # formula: output = input ^ gamma
    mapped = math.pow(normalized, gamma)
    # Scale back to original range
    return mapped * max_val

def brightness(num: int, c: float):
    check_init(True)
    # brightness remap based on 10^n
    r = gamma(map_duty_cycle(c))
    pwm[num].ChangeDutyCycle(100.0 - r)

def on(num: int):
    set(remap(num), LOW)

def off(num: int):
    set(remap(num), HIGH)

def flip(num: int):
    n = remap(num)
    set(n, not get(n))

__all__ = [
    "init", "release",
    "brightness", "on", "off", "flip",
    "L", "M", "R",
]
