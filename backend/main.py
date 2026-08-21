from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse


from src.motor_controller import motor_controller

app = FastAPI()
frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "tomoro-bot" / "dist"


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    mc = motor_controller.MotorController()

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            await websocket.send_text(f"You sent: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")


if frontend_dist.exists():
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        requested_file = (frontend_dist / full_path).resolve()
        dist_root = frontend_dist.resolve()

        if requested_file.is_relative_to(dist_root) and requested_file.is_file():
            return FileResponse(requested_file)

        return FileResponse(frontend_dist / "index.html")
