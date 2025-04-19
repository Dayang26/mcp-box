# main.py
import asyncio

from fastapi import FastAPI
from fastapi import WebSocket

from app.gateway.launcher import build_supergateway_command
from app.inspector.watcher import stream_logs
from app.process.manager import ProcessManager
from app.core.singleton import singleton_process_manager
from app.process.port_pool import get_available_port

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello MCP-Box!"}


@app.get("/test-port")
def test_port():
    port = get_available_port()
    return {"port": port}


@app.get("/process-manager")
async def process_manager():
    pm = ProcessManager()
    await pm.start_process("sleep 10", 3001)  # 示例：模拟一个“服务”
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
    pm = ProcessManager()
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


@app.websocket("/ws/logs/{port}")
async def websocket_logs(websocket: WebSocket, port: int):
    await stream_logs(websocket, port)
