# FCS细胞采样工具插件系统

FCS细胞采样工具支持插件系统，允许用户扩展软件功能，实现更多FCS数据处理功能。

## 插件使用方法

1. 在主界面中，切换到"插件功能"选项卡
2. 从下拉列表中选择要使用的插件
3. 点击"加载插件"按钮加载插件界面
4. 根据插件提供的界面进行操作
5. 在采样过程中，系统会自动应用选中的插件处理采样后的数据

## 插件管理

1. 在主界面中，切换到"插件管理"选项卡
2. 查看已安装的插件列表
3. 安装新插件：点击"浏览"选择插件ZIP文件，然后点击"安装插件"
4. 卸载插件：在插件列表中选择要卸载的插件，然后点击"卸载插件"

## 插件开发指南

### 基本要求

1. 插件必须继承自`FcsPluginInterface`类
2. 插件必须实现以下方法：
   - `get_info()`: 返回插件信息
   - `get_ui_elements(parent_frame)`: 返回插件UI元素
   - `process_fcs(metadata, raw_data, params=None)`: 处理FCS数据

### 插件结构

```python
from fcs_sampler_gui import FcsPluginInterface

class MyPlugin(FcsPluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "我的插件"
        self.description = "这是一个示例插件"
        self.version = "1.0.0"
        self.author = "开发者姓名"
        
    def get_info(self):
        """返回插件信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author
        }
    
    def get_ui_elements(self, parent_frame):
        """返回插件UI元素"""
        # 创建并返回插件UI
        # ...
        
    def process_fcs(self, metadata, raw_data, params=None):
        """处理FCS数据"""
        # 处理数据并返回结果
        # ...
        return processed_data, "处理描述"
```

### 打包插件

1. 将插件代码保存为Python文件（例如`my_plugin.py`）
2. 如果插件依赖其他模块，请将所有依赖文件一起打包
3. 将所有文件打包为ZIP文件
4. 使用"插件管理"选项卡中的"安装插件"功能安装

### 示例插件

本目录包含两个示例插件：

1. `fcs_gating_plugin.py`: 实现简单的细胞门控功能
2. `fcs_stats_plugin.py`: 实现FCS数据的统计分析功能

可以参考这些示例插件了解如何开发自己的插件。

## 注意事项

1. 插件应该处理可能的异常，避免影响主程序运行
2. 插件应该提供清晰的用户界面和操作说明
3. 插件应该返回处理后的数据和处理描述，以便主程序显示
4. 插件可能需要额外的Python库，请在插件文档中说明依赖 