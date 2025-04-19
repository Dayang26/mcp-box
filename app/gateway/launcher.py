# app/gateway/launcher.py

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
