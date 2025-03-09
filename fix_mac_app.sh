#!/bin/bash

# 设置应用程序路径
APP_PATH="dist/FCS细胞采样工具.app"

# 检查应用程序是否存在
if [ ! -d "$APP_PATH" ]; then
    echo "错误：找不到应用程序 $APP_PATH"
    exit 1
fi

echo "开始修复应用程序..."

# 设置权限
echo "设置权限..."
chmod -R 755 "$APP_PATH"

# 移除隔离属性
echo "移除隔离属性..."
xattr -rd com.apple.quarantine "$APP_PATH"

# 检查是否有签名问题
echo "检查签名..."
codesign --verify --verbose "$APP_PATH" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "应用程序签名无效，尝试重新签名..."
    codesign --force --deep --sign - "$APP_PATH"
fi

echo "修复完成！"
echo "现在尝试打开应用程序："
echo "open \"$APP_PATH\""

# 尝试打开应用程序
open "$APP_PATH"

echo ""
echo "如果应用程序仍然无法启动，请尝试以下步骤："
echo "1. 打开系统偏好设置 > 安全性与隐私"
echo "2. 在'通用'选项卡中，点击'仍要打开'按钮（如果显示）"
echo "3. 或者，尝试从终端运行应用程序："
echo "   $APP_PATH/Contents/MacOS/FCS细胞采样工具" 