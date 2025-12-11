from .gpio import *
from . import motor as Motor, led as LED

is_initialized = False

def initialize():
    global is_initialized
    print("Welcome to Movement GPIO, initializing...")
    # setup GPIO
    # use BCM pin numbering
    setmode(BCM)
    setwarnings(False)
    is_initialized = True

if not is_initialized:
    initialize()

# for compatibility
motor = Motor

__all__ = [
    "motor",
    "Motor",
    "LED"
]
