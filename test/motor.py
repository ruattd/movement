from time import sleep
from movement import *

motor_init()

# for _ in range(18):
#     motor_forward()
#     sleep(0.4)
#     motor_stop()
#     sleep(0.1)
#     motor_backward()
#     sleep(0.2)
#     motor_stop()
#     sleep(0.1)

motor_forward()
sleep(4)
motor_stop()