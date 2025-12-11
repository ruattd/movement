from time import sleep
from movement import *

# LED.init()

# for _ in range(10):
#     for x in range(3):
#         LED.flip(x)
#         sleep(0.2)

# LED.release()

LED.init(enable_brightness=True)

def ccn(n):
    return abs(100 - n % 200)

for i in range(0, 60 * 30):
    LED.brightness(LED.L, ccn(i))
    LED.brightness(LED.M, ccn(i + 20))
    LED.brightness(LED.R, ccn(i + 40))
    sleep(1 / 60)

# LED.brightness(LED.L, 50)
# sleep(5)

LED.release()
