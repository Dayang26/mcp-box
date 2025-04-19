# app/inspector/watcher.py
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.core.singleton import singleton_process_manager  # 🔁 引用共享单例



async def stream_logs(websocket: WebSocket, port: int):
    await websocket.accept()

    log_queue = singleton_process_manager.get_log_queue(port)
    if not log_queue:
        await websocket.send_text(f"[WebSocket Error] No running process at port {port}")
        await websocket.close()
        return

    try:
        while True:
            line = await log_queue.get()
            await websocket.send_text(line)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for port {port}")
    except Exception as e:
        await websocket.send_text(f"[WebSocket Error] {e}")
        await websocket.close()
