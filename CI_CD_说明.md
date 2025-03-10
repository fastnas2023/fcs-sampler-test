# GitHub Actions 自动构建说明

本项目使用GitHub Actions自动构建Mac和Windows平台的应用程序。以下是关于自动构建流程的详细说明。

## 工作流程概述

我们的GitHub Actions工作流程（`.github/workflows/build.yml`）包含三个主要任务：

1. **构建macOS应用程序**
2. **构建Windows应用程序**
3. **创建GitHub发布版本**

每当代码推送到主分支（main或master）或创建Pull Request时，自动构建流程将被触发。您也可以在GitHub界面手动触发工作流程。

## 构建产物

成功构建后，以下文件将作为构建产物提供：

- **macOS版本**：
  - `FCS细胞采样工具.app`（应用程序包）
  - `FCS细胞采样工具.dmg`（磁盘镜像安装文件）

- **Windows版本**：
  - `FCS细胞采样工具.exe`（可执行文件）
  - `FCS细胞采样工具_安装程序.exe`（NSIS安装程序）

## 如何使用

### 设置GitHub仓库

1. 在GitHub上创建一个新仓库
2. 将本项目代码推送到该仓库
3. 确保`.github/workflows/build.yml`文件包含在推送中

### 启用GitHub Actions

1. 在GitHub仓库页面，点击"Actions"选项卡
2. 如果看到提示，点击"I understand my workflows, go ahead and enable them"
3. 您应该能看到"Build FCS细胞采样工具"工作流程

### 触发构建

您可以通过以下方式触发构建：

1. **自动触发**：
   - 向主分支（main或master）推送代码
   - 创建指向主分支的Pull Request

2. **手动触发**：
   - 在GitHub仓库的"Actions"选项卡中
   - 选择"Build FCS细胞采样工具"工作流程
   - 点击"Run workflow"按钮
   - 选择分支并点击"Run workflow"

### 访问构建产物

1. **查看工作流程运行**：
   - 在GitHub仓库的"Actions"选项卡中
   - 点击最近的工作流程运行

2. **下载构建产物**：
   - 在工作流程运行页面底部的"Artifacts"部分
   - 点击"FCS细胞采样工具-macOS"或"FCS细胞采样工具-Windows"下载对应平台的构建产物

3. **从发布版本下载**：
   - 如果工作流程是由推送到主分支触发的，将自动创建一个新的发布版本
   - 在GitHub仓库的"Releases"选项卡中可以找到这些发布版本
   - 每个发布版本包含macOS和Windows平台的安装文件

## 自定义构建流程

如果需要自定义构建流程，可以编辑`.github/workflows/build.yml`文件：

- **修改触发条件**：更改`on`部分
- **更改Python版本**：修改`python-version`值
- **添加依赖项**：在`Install dependencies`步骤中添加更多pip包
- **调整构建参数**：修改PyInstaller或pynsist的参数
- **更改发布设置**：调整`Create Release`步骤的配置

## 故障排除

如果构建失败，请检查以下几点：

1. **查看工作流程日志**：
   - 在GitHub Actions运行页面查看详细日志
   - 找出失败的具体步骤和错误信息

2. **常见问题**：
   - **依赖项问题**：确保所有依赖项都已在工作流程中安装
   - **路径问题**：检查文件路径是否正确
   - **权限问题**：某些操作可能需要特定权限

3. **本地测试**：
   - 在本地环境中尝试构建步骤
   - 确认问题是否与GitHub Actions环境相关

## 高级配置

### 代码签名（macOS）

要为macOS应用程序添加代码签名，需要：

1. 在GitHub仓库设置中添加以下密钥：
   - `APPLE_CERTIFICATE_BASE64`：Base64编码的开发者证书
   - `APPLE_CERTIFICATE_PASSWORD`：证书密码
   - `APPLE_DEVELOPER_ID`：开发者ID

2. 修改工作流程文件，在构建macOS应用程序后添加签名步骤

### 自动版本号

当前工作流程使用GitHub运行编号作为版本号。如果需要更复杂的版本管理：

1. 创建一个版本文件（如`version.txt`）
2. 在工作流程中读取该文件
3. 使用读取的版本号创建发布版本

## 安全注意事项

- GitHub Actions工作流程可以访问仓库密钥
- 不要在工作流程文件中硬编码敏感信息
- 使用GitHub密钥存储敏感数据
- 小心审查第三方Actions的权限 