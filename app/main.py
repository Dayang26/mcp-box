# main.py
from fastapi import FastAPI

from app.process.port_pool import get_available_port

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello MCP-Box!"}


@app.get("/test-port")
def test_port():
    port = get_available_port()
    return {"port": port}
