from fastapi import APIRouter
from movement import motor

router = APIRouter()

@router.get("/init")
def init_motor():
    motor.init()
    return {"status": "initialized"}
