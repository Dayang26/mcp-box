# 使用官方 Python 3.11 slim 版镜像作为基础镜像
FROM python:3.11-slim

# 设置环境变量（修正语法警告）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装 curl、git、构建工具（为了后续安装某些包）
RUN apt-get update && apt-get install -y curl git build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖描述文件（先复制以利用 Docker 缓存）
COPY pyproject.toml requirements.txt ./

# 安装项目依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install uvicorn
# 确保 uvicorn 安装成功
RUN pip show uvicorn  # 显示 uvicorn 安装信息
RUN which uvicorn  # 确认 uvicorn 安装位置

# 复制项目文件
COPY . .

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 启动服务
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
