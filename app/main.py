# main.py
import asyncio
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.core.singleton import singleton_process_manager
from app.gateway.launcher import build_supergateway_command, build_command
from app.inspector.watcher import stream_logs
from app.models.types import LaunchConfig
from app.process.port_pool import get_available_port

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = Path(__file__).parent / "static" / "index.html"
    return index_path.read_text(encoding="utf-8")

@app.get("/test-port")
def test_port():
    port = get_available_port()
    return {"port": port}


@app.get("/process-manager")
async def process_manager():
    pm = singleton_process_manager

    await pm.start_process("sleep 10", 3001)
    await asyncio.sleep(3)
    print("当前进程：", pm.list_running())
    await pm.stop_process(3001)


@app.get("/process-supergateway")
async def process_supergateway():
    cmd = (
        'npx -y supergateway '
        '--stdio "npx -y @modelcontextprotocol/server-filesystem /Users/aaronhu/PycharmProjects/mcp-box" '
        '--port 8001'
    )
    pm = singleton_process_manager

    await pm.start_process(cmd, 8001)
    await asyncio.sleep(3)
    print("当前进程：", pm.list_running())
    await pm.stop_process(8001)


@app.get("/launch-command")
def launch_command():
    cmd = build_supergateway_command("/Users/aaronhu/PycharmProjects/mcp-box", 8001)
    return {"command": cmd}


@app.get("/start-supergateway")
async def start_supergateway():
    tool_path = "/Users/aaronhu/PycharmProjects/mcp-box"
    port = 8001  # 实际中应来自 port_pool
    cmd = build_supergateway_command(tool_path, port)

    await singleton_process_manager.start_process(cmd, port)
    await asyncio.sleep(3000)
    print("当前进程：", singleton_process_manager.list_running())
    await singleton_process_manager.stop_process(port)

    return {"status": "started", "port": port}


# @app.post("/start-process")
# async def start_process(config: LaunchConfig):
#     cmd, port = build_command(config)
#     print(f"xxxxxx   {cmd} --port={port}")
#     await singleton_process_manager.start_process(cmd, port)
#     await asyncio.sleep(3000 )
#
#     print("当前进程：", singleton_process_manager.list_running())
#     await singleton_process_manager.stop_process(port)
#
#     return {"status": "started", "port": port}

@app.post("/start-process")
async def start_process(config: LaunchConfig):
    print(f"xxxxxxxxxxxxxxxxxxxxxx")
    cmd, port = build_command(config)
    await singleton_process_manager.start_process(cmd, port)
    return {"status": "started", "port": port}


@app.post("/stop-process/{port}")
async def stop_process(port: int):
    try:
        await singleton_process_manager.stop_process(port)
        return {"status": "stopped", "port": port}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No process running on port {port}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/running-processes")
def list_running():
    return singleton_process_manager.list_running()


@app.websocket("/ws/logs/{port}")
async def websocket_logs(websocket: WebSocket, port: int):
    await stream_logs(websocket, port)
