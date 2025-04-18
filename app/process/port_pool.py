import random
import socket

PORT_RANGE = (3000, 3999)

used_ports = set()


def is_port_available(port: int) -> bool:
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def get_available_port() -> int:
    """返回一个可用端口"""
    for _ in range(100):
        port = random.randint(*PORT_RANGE)
        temp = is_port_available(port)
        print(f"port {port} is available {temp}")
        if port not in used_ports and temp:
            used_ports.add(port)
            return port
    raise RuntimeError('no available port')
