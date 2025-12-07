import RPi.GPIO as R

print("Welcome to Movement GPIO, initializing...")

# setup GPIO
# use BCM pin numbering
R.setmode(R.BCM)
R.setwarnings(False)

from .pin_definition import *
from . import motor
