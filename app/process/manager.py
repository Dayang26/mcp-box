import asyncio
from typing import Optional


class ProcessInfo:
    def __init__(self, command: str, port: int):
        self.command = command
        self.port = port
        self.process: Optional[asyncio.subprocess.Process] = None


class ProcessManager:
    def __init__(self):
        self.processes: dict[int, ProcessInfo] = {}

    async def start_process(self, command: str, port: int):
        """启动子进程并切记录状态"""
        if port in self.processes:
            raise ValueError(f"Port {port} is already in use")

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        self.processes[port] = ProcessInfo(command, port)
        self.processes[port].process = process
        print(f"successful to start {command} ({port})")
        return process

    async def stop_process(self, port: int):
        """终止子进程"""
        info = self.processes[port]
        if info and info.process:
            info.process.terminate()
            await info.process.wait()
            print(f"successful to stop {info.command} ({port})")
            self.processes.pop(port, None)

    def list_running(self):
        """列出所有正在运行的进程"""
        return [
            {"port": p, "cmd": info.command, "running": not info.process.returncode}
            for p, info in self.processes.items()
            if info.process and info.process.returncode is None
        ]
