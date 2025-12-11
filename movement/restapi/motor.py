from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from movement import motor
from . import secrets
import struct

router = APIRouter()

control_secret: str | None = None

@router.get("/init")
def initialize():
    """
    Initialize the motor and get control secret.
    """
    global control_secret
    if control_secret == None:
        print("[Movement][Motor] Initializing...")
        motor.init()
        control_secret = secrets.generate_secret(32)
        print(f"[Movement][Motor] Control secret: {control_secret}")
        return {
            "status": "initialized",
            "secret": control_secret
        }
    else:
        print("[Movement][Motor] Already initialized, rejected")
        return {
            "status": "already_initialized",
            "message": "Motor control has already been initialized, please call '/dispose' first."
        }

def check_secret(secret: str | None):
    if control_secret == None:
        print(f"[Movement][Motor] Not initialized, rejected")
        return {
            "status": "not_initialized",
            "message": "Please call '/init' and get control secret first."
        }
    elif secret == control_secret:
        return None
    else:
        print(f"[Movement][Motor] Invalid secret: {secret}")
        return {
            "status": "invalid_secret",
            "message": "Invalid control secret."
        }

@router.post("/dispose")
def dispose(secret: str | None = None):
    """
    Dispose the motor control and invalidate the secret.
    
    :param secret: Control secret
    :type secret: str | None
    """
    global control_secret
    check = check_secret(secret)
    if check:
        return check
    motor.release()
    control_secret = None
    print("[Movement][Motor] Control disposed")
    return {
        "status": "successful",
        "message": "Motor control disposed."
    }

@router.post("/forward")
def forward(secret: str | None = None):
    """
    Request forward.
    
    :param secret: Control secret
    :type secret: str | None
    """
    check = check_secret(secret)
    if check:
        return check
    motor.forward()
    print("[Movement][Motor] Forward")

@router.post("/backward")
def backward(secret: str | None = None):
    """
    Request backward.
    
    :param secret: Control secret
    :type secret: str | None
    """
    check = check_secret(secret)
    if check:
        return check
    motor.backward()
    print("[Movement][Motor] Backward")

@router.post("/turn-left")
def turn_left(secret: str | None = None):
    """
    Request turn left.
    
    :param secret: Control secret
    :type secret: str | None
    """
    check = check_secret(secret)
    if check:
        return check
    motor.turn_left()
    print("[Movement][Motor] Turn left")

@router.post("/turn-right")
def turn_right(secret: str | None = None):
    """
    Request turn right.
    
    :param secret: Control secret
    :type secret: str | None
    """
    check = check_secret(secret)
    if check:
        return check
    motor.turn_right()
    print("[Movement][Motor] Turn right")

@router.post("/stop")
def stop(secret: str | None = None):
    """
    Request stop.
    
    :param secret: Control secret
    :type secret: str | None
    """
    check = check_secret(secret)
    if check:
        return check
    motor.stop()
    print("[Movement][Motor] Stop")

def check_data_range(x: float, y: float):
    if x < -1 or x > 1 or y < -1 or y > 1:
        errmsg = f"Invalid data range sent by client: expect -1.0 ~ 1.0, actual ({x}, {y})"
        print(f"[Movement][Motor] {errmsg}")
        return {
            "status": "invalid_data_range",
            "message": errmsg
        }
    return None

@router.post("/map")
def map(secret: str | None = None, x: float = 0.0, y: float = 0.0):
    """
    Control motor by map API.
    
    :param secret: Control secret
    :type secret: str | None
    :param x: Map X, -1.0 (left) ~ 1.0 (right)
    :type x: float
    :param y: Map Y, -1.0 (forward) ~ 1.0 (backward)
    :type y: float
    """
    check = check_secret(secret)
    if check:
        return check
    check_range = check_data_range(x, y)
    if check_range:
        return check_range
    motor.map(x, y)
    print(f"[Movement][Motor] Set map: ({x}, {y})")

@router.websocket("/map/ws")
async def map_control(ws: WebSocket, secret: str | None = None):
    """
    Connect to map control API through web socket.
    
    :param secret: Control secret
    :type secret: str
    """
    try:
        print(f"[Movement][Motor] New client trying to connect: {ws.headers.get("User-Agent")}")
        await ws.accept()
        check = check_secret(secret)
        if check:
            await ws.send_json(check)
            await ws.close()
            return
        print("[Movement][Motor] Map API connected")
        FORMAT_STR = "<dd"
        EXPECTED_LEN = 16
        while True:
            data = await ws.receive_bytes()
            if len(data) != EXPECTED_LEN:
                errmsg = f"Invalid data length sent by client: expect {EXPECTED_LEN}, actual {len(data)}"
                print(f"[Movement][Motor] {errmsg}")
                await ws.send_json({
                    "status": "invalid_data_length",
                    "message": errmsg
                })
                await ws.close()
                break
            unpacked = struct.unpack(FORMAT_STR, data)
            x = unpacked[0]
            y = unpacked[1]
            check_range = check_data_range(x, y)
            if check_range:
                await ws.send_json(check_range)
                await ws.close()
                break
            motor.map(x, y)
        print("[Movement][Motor] Connection closed")
    except WebSocketDisconnect as e:
        print(f"[Movement][Motor] Client disconnected: {e.code}")
    motor.map(0, 0)
