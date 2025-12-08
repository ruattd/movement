from fastapi import FastAPI

app = FastAPI(title="Movement GPIO")

@app.get("/")
def index():
    """
    Root endpoint returning a welcome message.
    """
    return {"message": "Welcome to Movement GPIO REST API!"}

# motor driving endpoints
from .motor import router as motor_router
app.include_router(motor_router, prefix="/motor")
