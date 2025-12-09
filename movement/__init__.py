from .gpio import *
from . import motor

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
