from time import sleep
from movement import *

motor.init()

motor.speed_left(100)
motor.speed_right(20)
motor.forward()
sleep(4)
motor.stop()
