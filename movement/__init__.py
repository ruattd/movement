import RPi.GPIO as R

is_initialized = False

def initialize():
    global is_initialized
    print("Welcome to Movement GPIO, initializing...")
    # setup GPIO
    # use BCM pin numbering
    R.setmode(R.BCM)
    R.setwarnings(False)
    is_initialized = True

if not is_initialized:
    initialize()

from .pin_definition import *
from . import motor
