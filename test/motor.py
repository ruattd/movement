from time import sleep
from movement import *

motor.init()

for _ in range(6):
    motor.speed_left(100)
    motor.speed_right(100)
    motor.turn_left()
    sleep(0.5)
    motor.stop()
    sleep(0.1)
    motor.forward()
    sleep(0.5)
    motor.stop()
    sleep(0.1)
    motor.speed_left(50)
    motor.speed_right(50)
    motor.turn_left()
    sleep(0.5)
    motor.stop()
    sleep(0.1)
    motor.forward()
    sleep(0.5)
    motor.stop()
    sleep(0.1)
