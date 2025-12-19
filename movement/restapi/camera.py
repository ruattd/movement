import cv2, av, fractions
from cv2 import VideoCapture
from av import CodecContext, VideoFrame
from fractions import Fraction
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from . import secrets

route = APIRouter()

@route.get("/test")
def test(
    device: int = 0,
    width: int | None = None,
    height: int | None = None,
    fps: int | None = None,
):
    """
    Test video arguments and get the actually used arguments
    """
    try:
        cap = VideoCapture(device)
        if width: cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if fps: cap.set(cv2.CAP_PROP_FPS, fps)
        result = {
            "status": "success",
            "arguments": {
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": int(cap.get(cv2.CAP_PROP_FPS)),
                "pixfmt": cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT),
            },
        }
        cap.release()
        return result
    except Exception as e:
        return {
            "status": "failed",
            "exception": str(type(e)),
            "message": str(e),
        }

captures: dict[str, VideoCapture] = {}
codecs: dict[str, CodecContext] = {}

def release():
    for _, cap in captures.items():
        cap.release()
    cv2.destroyAllWindows()

@route.post("/open")
def open(
    device: int = 0,
    width: int | None = None,
    height: int | None = None,
    fps: int | None = None,
    codec: str = "libx264",
    pixfmt: str = "yuv420p",
    bitrate: int = 2000,
    preset: str = "ultrafast",
    tune: str = "zerolatency",
):
    """
    Open video capture and get web socket secret.
    """
    print(f"[Movement][Camera] Initializing video capture on device {device}...")
    secret = secrets.generate_secret(32)
    _cap = VideoCapture(device)
    print(f"[Movement][Camera] Capture arguments to apply: width = {width}, height = {height}, fps = {fps}")
    if width: _cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height: _cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if fps: _cap.set(cv2.CAP_PROP_FPS, fps)
    print(f"[Movement][Camera] Initializing video encoding with '{codec}' codec and '{pixfmt}' pixel format...")
    _codec = CodecContext.create(codec, "w")
    _codec.options = {
        "preset": preset,
        "tune": tune,
        "width": str(int(_cap.get(cv2.CAP_PROP_FRAME_WIDTH))),
        "height": str(int(_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
        "pix_fmt": pixfmt,
    }
    _codec.time_base = Fraction(1, fps)
    _codec.bit_rate = bitrate * 1000
    captures[secret] = _cap
    codecs[secret] = _codec
    print(f"[Movement][Camera] Video capture initialized with secret: {secret}")
    return {
        "status": "success",
        "secret": secret,
    }

def check_secret(secret: str):
    if captures[secret]:
        return None
    elif len(captures) == 0:
        print(f"[Movement][Camera] No open capture, rejected")
        return {
            "status": "not_initialized",
            "message": "Please call '/open' and get capture secret first."
        }
    else:
        print(f"[Movement][Camera] Invalid secret: {secret}")
        return {
            "status": "invalid_secret",
            "message": "Invalid control secret."
        }

@route.post("/close")
def close(secret: str):
    """
    Close video capture
    """
    if check := check_secret(secret):
        return check
    cap = captures[secret]
    cap.release()
    captures.pop(secret)
    codecs.pop(secret)
    print(f"[Movement][Camera] Capture closed with secret: {secret}")

@route.websocket("/stream")
async def stream(ws: WebSocket, secret: str):
    """
    Receive the video stream.
    """
    if check := check_secret(secret):
        return check
    cap = captures[secret]
    codec = codecs[secret]
    await ws.accept()
    try:
        frame_count = 0
        while True:
            ret, img = cap.read()
            if not ret: break
            # TODO
    except WebSocketDisconnect as e:
        print(f"[Movement][Camera] Client disconnected: {e.code}")
        print("[Movement][Camera] Closing the capture...")
        close(secret)
