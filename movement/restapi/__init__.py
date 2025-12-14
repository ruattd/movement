from fastapi import FastAPI

app = FastAPI(
    title="Movement",
    description="REST API for taking the control of your RS bot based on Raspberry Pi",
)

@app.get("/")
def index():
    """
    Root endpoint returning a welcome message.
    """
    return {"message": "Welcome to Movement GPIO REST API!"}

from . import motor, camera

# motor control endpoints
app.include_router(motor.route, prefix="/motor")

# video capture endpoints
app.include_router(camera.route, prefix="/cam")

def release():
    camera.release()
