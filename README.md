# FCS细胞采样工具

## 项目简介

FCS细胞采样工具是一个用于处理和分析流式细胞仪（Flow Cytometry）数据的应用程序。该工具可以从FCS文件中提取样本数据，并根据用户指定的参数进行采样和分析。

## 功能特点

- 支持从FCS文件中读取和处理流式细胞仪数据
- 提供多种采样方式：随机采样、范围采样、固定步长采样等
- 用户友好的图形界面，简化操作流程
- 支持Windows和macOS平台
- 导出采样结果为新的FCS文件，便于后续分析

## 安装方法

### Windows用户

1. 从[最新发布版本](https://github.com/fastnas2023/fcs-sampler-test/releases/latest)下载Windows安装程序（`FCS细胞采样工具_vX.X.X_安装程序.exe`）
2. 双击安装程序，按照提示完成安装
3. 从开始菜单或桌面快捷方式启动应用程序

### macOS用户

1. 从[最新发布版本](https://github.com/fastnas2023/fcs-sampler-test/releases/latest)下载macOS安装包（`FCS细胞采样工具_vX.X.X.dmg`）
2. 打开DMG文件，将应用程序拖到Applications文件夹
3. 从Applications文件夹或Launchpad启动应用程序

## 使用说明

1. 启动应用程序
2. 点击"选择FCS文件"按钮，选择要处理的FCS文件
3. 选择采样方式（随机采样、范围采样或固定步长采样）
4. 设置采样参数
5. 点击"开始采样"按钮
6. 采样完成后，点击"保存结果"按钮，将结果保存为新的FCS文件

## 开发环境

- Python 3.12
- 依赖库：numpy, pandas, fcsparser, flowio, tkinter, PIL, matplotlib, scipy, FlowCytometryTools

## 版本历史

当前版本：v1.0.2

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。

## 贡献

欢迎提交问题报告和功能建议。如果您想为项目做出贡献，请提交Pull Request。
