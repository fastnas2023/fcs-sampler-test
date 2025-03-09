FROM python:3.9-windowsservercore

# 设置工作目录
WORKDIR /app

# 复制所需文件
COPY fcs_sampler_gui.py .
COPY FCS细胞采样工具_windows.spec .
COPY windows_hook.py .
COPY app_icon.ico .

# 安装依赖
RUN pip install pyinstaller numpy pandas fcsparser flowio pillow setuptools wheel
RUN pip install git+https://github.com/eyurtsev/FlowCytometryTools.git

# 运行打包命令
CMD ["pyinstaller", "FCS细胞采样工具_windows.spec"] 