# app/gateway/launcher.py
from app.models.types import LaunchConfig
from app.process.port_pool import get_available_port


def build_supergateway_command(tool_path: str, port: int) -> str:
    """
    构造启动 supergateway 命令
    :param tool_path: 本地工具路径
    :param port: 分配的端口号
    :return: 可用于subprocess 执行的命令字符串
    """
    # 外层需要一对双引号包裹整个命令，内层路径要转义
    safe_path = tool_path.replace('"', '\\"')  # 转义双引号
    inner = f'npx -y @modelcontextprotocol/server-filesystem \\"{safe_path}\\"'
    cmd = f'npx -y supergateway --stdio "{inner}" --port {port}'
    return cmd


def build_command(config: LaunchConfig) -> tuple[str, int]:
    """
    根据用户提供的配置构建 supergateway 启动命令
    :param config: 用户提交的命令启动配置
    :return: 构建好的 supergateway 命令字符串 和 实际使用的端口
    """
    port = config.port or get_available_port()

    safe_args = [arg.replace('"', '\\"') for arg in config.args]
    inner_command = f'{config.command} {" ".join(safe_args)}'

    cmd_str = f'npx -y supergateway --stdio "{inner_command}" --port {port}'

    return cmd_str, port