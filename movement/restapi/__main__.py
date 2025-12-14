import uvicorn
import argparse

def main():
    # parse command-line arguments
    parser = argparse.ArgumentParser(description="Start the FastAPI server.")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host address to bind to."
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port to bind to."
    )
    parser.add_argument(
        "--reload", "-r",
        action="store_true", # 这是一个布尔标志
        help="Enable auto-reload for development."
    )
    args = parser.parse_args()

    # start the server
    uvicorn.run(
        "movement.restapi:app", 
        host=args.host, 
        port=args.port,
        reload=args.reload,
        ws_ping_interval=2,
        ws_ping_timeout=4,
    )

    # release resources
    from . import release
    release()

if __name__ == "__main__":
    main()
