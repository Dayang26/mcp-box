# app/process/manager.py

import asyncio
from typing import Optional


class ProcessInfo:
    def __init__(self, command: str, port: int):
        self.command = command
        self.port = port
        self.process: Optional[asyncio.subprocess.Process] = None
        self.log_queue: Optional[asyncio.Queue] = None


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
            stderr=asyncio.subprocess.STDOUT,
        )

        info = ProcessInfo(command, port)
        info.process = process
        info.log_queue = asyncio.Queue()
        self.processes[port] = info

        asyncio.create_task(self._read_logs_to_queue(process, info.log_queue))
        print(f"successful to start {command} ({port})")
        return process

    async def _read_logs_to_queue(self, process: asyncio.subprocess.Process, queue: asyncio.Queue):
        """从 stdout 异步读取日志并写入队列"""
        try:
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                await queue.put(line.decode("utf-8").rstrip())
        except Exception as e:
            await queue.put(f"[error] Failed reading log: {e}")

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

    def get_log_queue(self, port: int) -> Optional[asyncio.Queue]:
        """获取日志用于队列 WebSocket 推送"""
        info = self.processes.get(port)
        return info.log_queue if info else None
