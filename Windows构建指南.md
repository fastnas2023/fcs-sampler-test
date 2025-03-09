# Windows构建指南

本指南将帮助你在Windows系统上构建FCS细胞采样工具的可执行文件。

## 准备工作

1. 确保你的Windows系统已安装Python 3.9或更高版本
2. 将整个项目文件夹复制到Windows系统上

## 安装依赖项

打开命令提示符（CMD）或PowerShell，进入项目目录，然后运行以下命令：

```
pip install pyinstaller numpy pandas fcsparser flowio pillow matplotlib scipy
pip install git+https://github.com/eyurtsev/FlowCytometryTools.git
```

## 构建应用程序

在项目目录中，运行以下命令：

```
pyinstaller FCS细胞采样工具_windows.spec
```

或者，你也可以运行：

```
python -m PyInstaller FCS细胞采样工具_windows.spec
```

## 构建结果

构建完成后，可执行文件将位于`dist`文件夹中，名为`FCS细胞采样工具.exe`。

## 常见问题

### 如果应用程序无法启动

1. 确保你已安装所有必要的依赖项
2. 尝试从命令行运行应用程序，查看错误信息
3. 检查Windows安全设置，可能需要允许运行未签名的应用程序

### 如果缺少DLL文件

如果运行时提示缺少DLL文件，可能需要安装Visual C++ Redistributable：
- 下载并安装最新的Visual C++ Redistributable：https://aka.ms/vs/17/release/vc_redist.x64.exe

## 使用Docker构建（可选）

如果你有Docker环境，也可以使用Docker构建Windows应用程序：

1. 安装Docker
2. 在项目目录中运行：
   ```
   docker build -t fcs-builder .
   docker run --name fcs-build fcs-builder
   docker cp fcs-build:/app/dist/FCS细胞采样工具.exe .
   docker rm fcs-build
   ```

## 故障排除

如果遇到问题，请尝试以下步骤：

1. 删除`build`和`dist`文件夹，然后重新构建
2. 确保使用的是最新版本的PyInstaller
3. 检查Windows事件查看器中的错误信息 