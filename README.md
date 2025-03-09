# FCS细胞采样工具

## 项目概述
FCS细胞采样工具是一个用于处理和采样FCS（Flow Cytometry Standard）文件的图形界面应用程序。该工具允许用户以多种方式从FCS文件中采样细胞数据，支持跨平台运行（Windows和macOS）。

## 技术栈
- Python 3.12
- GUI框架：Tkinter
- 数据处理：numpy、pandas
- FCS文件处理：fcsparser、flowio
- 打包工具：PyInstaller

## 功能特性
1. 图形用户界面
   - 直观的文件选择界面
   - 实时信息显示区域
   - 清晰的参数设置面板

2. 采样功能
   - 支持多种采样模式：
     * 连续采样：从指定位置开始连续获取细胞
     * 间隔采样：按固定间隔采样细胞
     * 随机采样：随机选择指定数量的细胞
   - 灵活的范围设置：
     * 可指定起始和结束位置
     * 支持设置目标采样数量

3. 文件处理
   - 支持FCS格式文件的读取和写入
   - 自动保存采样结果为新的FCS文件
   - 保留原始文件的元数据信息

## 项目结构
```
├── fcs_sampler_gui.py    # 主程序GUI界面
├── process_fcs.py        # FCS文件处理核心功能
├── build_app.py         # 应用打包脚本（通用）
├── build_windows.py     # Windows版本打包脚本
├── windows_hook.py      # Windows特定运行时钩子
├── app_icon.ico         # Windows图标文件
├── app_icon.icns        # macOS图标文件
├── Dockerfile           # Windows版本Docker构建文件
└── build_with_docker.sh # Docker构建脚本
```

## 构建说明

### macOS版本构建
```bash
python build_app.py
```

### Windows版本构建
1. 直接构建：
```bash
python build_windows.py
```

2. 使用Docker构建：
```bash
./build_with_docker.sh
```

## 使用说明
1. 启动应用程序
2. 点击"选择文件"按钮选择要处理的FCS文件
3. 设置采样参数：
   - 设置采样范围（起始位置和结束位置）
   - 设置目标采样数量
   - 选择采样模式（连续、间隔或随机）
4. 点击"开始采样"按钮开始处理
5. 处理完成后，采样结果将自动保存为新的FCS文件

## 依赖环境
- Python 3.12+
- numpy
- pandas
- fcsparser
- flowio
- Pillow
- PyInstaller（仅构建需要）

## 注意事项
- 确保有足够的磁盘空间存储输出文件
- 大文件处理可能需要较长时间，请耐心等待
- 建议在处理大文件时先使用小文件测试所选参数