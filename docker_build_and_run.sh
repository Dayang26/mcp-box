#!/bin/bash

set -e

IMAGE_NAME="mcp-box"
CONTAINER_NAME="mcp-box-dev"

echo "🧼 清理旧容器..."
if [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    docker rm -f $CONTAINER_NAME
    echo "🗑️ 已移除旧容器: $CONTAINER_NAME"
fi

echo "🧼 清理旧镜像..."
if docker images | grep -q "^${IMAGE_NAME}"; then
    docker rmi $IMAGE_NAME
    echo "🗑️ 已移除旧镜像: $IMAGE_NAME"
fi

echo "🔨 构建新镜像..."
docker build -t $IMAGE_NAME .

echo "🚀 启动新容器..."
docker run -d --rm \
    -p 8000:8000 \
    --name $CONTAINER_NAME \
    $IMAGE_NAME

echo "✅ 容器已启动：http://localhost:8000"
