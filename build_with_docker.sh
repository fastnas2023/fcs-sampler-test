#!/bin/bash

# 构建 Docker 镜像
docker build -t fcs-builder .

# 运行容器并复制生成的 exe
docker run --name fcs-build fcs-builder
docker cp fcs-build:/app/dist/FCS细胞采样工具.exe .
docker rm fcs-build 