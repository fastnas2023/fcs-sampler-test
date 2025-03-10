# FCS细胞采样工具

FCS细胞采样工具是一个用于处理流式细胞仪数据的应用程序。它可以帮助您从大型FCS文件中提取样本，支持多种采样模式。

## 下载安装

### 最新版本：v1.0.3

- **Windows版本**：
  - [Windows安装程序(.exe)](https://github.com/fastnas2023/fcs-sampler-test/releases/download/v1.0.3/FCS细胞采样工具_v1.0.3_安装程序.exe)
  - [Windows可执行文件(.exe)](https://github.com/fastnas2023/fcs-sampler-test/releases/download/v1.0.3/FCS细胞采样工具_v1.0.3.exe)

- **macOS版本**：
  - [macOS安装包(.dmg)](https://github.com/fastnas2023/fcs-sampler-test/releases/download/v1.0.3/FCS细胞采样工具_v1.0.3.dmg)

- [查看所有版本](https://github.com/fastnas2023/fcs-sampler-test/releases)

## 功能特点

- 支持多种采样模式：
  - 连续采样：从指定位置开始连续提取指定数量的细胞
  - 间隔采样：按固定间隔从指定范围内提取细胞
  - 随机采样：从指定范围内随机提取指定数量的细胞
- 直观的图形用户界面
- 实时处理信息显示
- 自动检查更新
- **插件系统**：支持通过插件扩展功能，实现更多FCS数据处理

## 安装方法

### Windows

1. 下载最新的[安装包(.exe)](https://github.com/fastnas2023/fcs-sampler-test/releases/download/v1.0.3/FCS细胞采样工具_v1.0.3_安装程序.exe)
2. 双击安装包运行安装程序
3. 按照安装向导完成安装

### macOS

1. 下载最新的[应用包(.dmg)](https://github.com/fastnas2023/fcs-sampler-test/releases/download/v1.0.3/FCS细胞采样工具_v1.0.3.dmg)
2. 打开dmg文件
3. 将应用拖到Applications文件夹

### 从源码运行

1. 克隆或下载本仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行程序：`python fcs_sampler_gui.py`

## 详细运行方法

### 环境准备

1. 确保已安装Python 3.7或更高版本
   - 检查Python版本：`python --version`
   - 如果没有安装Python，请从[Python官网](https://www.python.org/downloads/)下载并安装

2. 建议使用虚拟环境（可选但推荐）
   ```bash
   # 创建虚拟环境
   python -m venv .venv
   
   # 激活虚拟环境
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

### 运行程序

#### Windows

```bash
# 在命令提示符或PowerShell中
cd 项目目录路径
python fcs_sampler_gui.py
```

#### macOS

```bash
# 在终端中
cd /Users/用户名/项目目录路径
python fcs_sampler_gui.py
```
或者
```bash
cd ~/项目目录路径
python fcs_sampler_gui.py
```

#### Linux

```bash
# 在终端中
cd /home/用户名/项目目录路径
python fcs_sampler_gui.py
```

### 常见问题

1. **依赖安装失败**
   - 确保pip已更新到最新版本：`pip install --upgrade pip`
   - 尝试单独安装失败的依赖：`pip install 依赖名称`

2. **程序启动失败**
   - 检查Python版本是否兼容
   - 确保所有依赖都已正确安装
   - 查看错误信息，根据提示解决问题

3. **GUI显示异常**
   - 在某些Linux发行版上，可能需要安装额外的Tk包：`sudo apt-get install python3-tk`（Ubuntu/Debian）或`sudo dnf install python3-tkinter`（Fedora）

4. **插件加载失败**
   - 确保插件文件放置在正确的目录（`plugins/`）
   - 检查插件代码是否符合插件接口规范

## 使用方法

1. 启动应用程序
2. 选择FCS文件和输出目录
3. 设置采样参数：
   - 起始位置：从哪个细胞开始采样
   - 结束位置：到哪个细胞结束采样（-1表示到文件末尾）
   - 目标细胞数：要提取的细胞数量（-1表示全部）
   - 采样模式：连续采样、间隔采样或随机采样
4. 点击"开始采样"按钮
5. 查看处理信息和结果

## 插件系统

FCS细胞采样工具支持插件系统，允许用户扩展软件功能，实现更多FCS数据处理功能。

### 使用插件

1. 在主界面中，切换到"插件功能"选项卡
2. 从下拉列表中选择要使用的插件
3. 点击"加载插件"按钮加载插件界面
4. 根据插件提供的界面进行操作
5. 在采样过程中，系统会自动应用选中的插件处理采样后的数据

### 管理插件

1. 在主界面中，切换到"插件管理"选项卡
2. 查看已安装的插件列表
3. 安装新插件：点击"浏览"选择插件ZIP文件，然后点击"安装插件"
4. 卸载插件：在插件列表中选择要卸载的插件，然后点击"卸载插件"

### 内置插件

- **FCS门控插件**：对FCS数据进行门控分析，可以根据指定参数筛选细胞
- **FCS统计分析插件**：对FCS数据进行统计分析，包括直方图、基本统计量等

### 开发插件

如果您想开发自己的插件，请参考 `plugins/README.md` 文件中的插件开发指南。

## 支持与反馈

如果您在使用过程中遇到问题，或有任何建议，请通过以下方式联系我们：

- 提交GitHub Issue
- 发送邮件至：support@example.com

## 打赏支持

如果您觉得这个工具对您有所帮助，欢迎扫描下方二维码进行打赏支持！您的支持将帮助我们持续改进和维护这个工具。

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="qrcode-wechat-small.png" alt="微信支付" width="300"/>
        <p>WeChat(微信)</p>
      </td>
      <td align="center">
        <img src="qrcode-alipay-small.png" alt="支付宝" width="300"/>
        <p>Alipay(支付宝)</p>
      </td>
    </tr>
  </table>
</div>

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。
