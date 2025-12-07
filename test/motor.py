from time import sleep
from movement import *

motor_init()

for _ in range(18):
    motor_turnleft()
    sleep(0.5)
    motor_stop()
    sleep(0.1)
    motor_forward()
    sleep(0.5)
    motor_stop()
    sleep(0.1)
