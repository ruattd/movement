### GPIO IMPORTS ###

try:
    import RPi.GPIO as G
except Exception:
    import Mock.GPIO as G

setmode = G.setmode
setwarnings = G.setwarnings
setup = G.setup
set = G.output
get = G.input
PWM = G.PWM
HIGH = G.HIGH
LOW = G.LOW
OUT = G.OUT
IN = G.IN
BCM = G.BCM
BOARD = G.BOARD

### PIN DEFINITIONS ###

# LED
LED0 = 10
LED1 = 9
LED2 = 25

# Motor
EN_L = 13
EN_R = 20
IN_RF = 19
IN_RB = 16
IN_LF = 21
IN_LB = 26
