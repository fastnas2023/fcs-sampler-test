import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fcsparser import parse
import flowio
import numpy as np
from datetime import datetime
import os
import tempfile
from PIL import Image, ImageTk  # 添加PIL库导入
import webbrowser  # 添加webbrowser库用于打开网页链接
import requests  # 添加requests库用于网络请求
import json  # 添加json库用于解析API响应
import threading  # 添加threading库用于后台任务
import re  # 添加re库用于版本比较
import importlib.util  # 用于动态导入插件
import inspect  # 用于检查插件类
import pkgutil  # 用于遍历插件包
import sys  # 用于添加插件路径
import zipfile  # 用于处理插件zip文件
import shutil  # 用于文件操作
import locale  # 用于获取系统语言设置


# 添加多语言支持
class I18n:
    """国际化支持类，用于管理多语言翻译"""

    def __init__(self):
        # 默认语言为中文
        self.current_lang = "zh_CN"
        # 尝试获取系统语言
        try:
            system_lang, _ = locale.getdefaultlocale()
            if system_lang:
                if system_lang.startswith("en"):
                    self.current_lang = "en_US"
                elif system_lang.startswith("zh"):
                    self.current_lang = "zh_CN"
        except:
            pass

        # 加载翻译资源
        self.translations = {
            "zh_CN": self._load_chinese(),
            "en_US": self._load_english(),
        }

    def _load_chinese(self):
        """加载中文翻译"""
        return {
            "app_title": "FCS文件细胞采样工具",
            "check_update": "检查更新",
            "developed_by": "由",
            "studio": "工作室开发",
            # 选项卡标题
            "tab_sampling": "采样设置",
            "tab_plugins": "插件功能",
            "tab_plugin_mgmt": "插件管理",
            "tab_about": "关于与支持",
            # 文件设置
            "file_settings": "文件设置",
            "fcs_file": "FCS文件:",
            "browse": "浏览...",
            "output_dir": "输出目录:",
            # 采样参数
            "sampling_params": "采样参数",
            "start_pos": "起始位置:",
            "end_pos": "结束位置:",
            "end_pos_hint": "(-1表示到文件末尾)",
            "target_count": "目标细胞数:",
            "target_count_hint": "(-1表示全部)",
            "sample_mode": "采样模式:",
            "continuous": "连续采样",
            "interval": "间隔采样",
            "random": "随机采样",
            # 按钮
            "start_sampling": "开始采样",
            "clear_info": "清除信息",
            # 处理信息
            "process_info": "处理信息",
            # 插件功能
            "select_plugin": "选择插件",
            "available_plugins": "可用插件:",
            "load_plugin": "加载插件",
            "plugin_desc": "插件描述",
            "select_plugin_hint": "请选择一个插件以查看描述",
            "plugin_function": "插件功能",
            "load_plugin_hint": "请先选择并加载一个插件",
            # 插件管理
            "installed_plugins": "已安装插件",
            "refresh_list": "刷新列表",
            "uninstall_plugin": "卸载插件",
            "install_new_plugin": "安装新插件",
            "plugin_file": "插件文件:",
            "install_plugin": "安装插件",
            "plugin_dev": "插件开发",
            "plugin_dev_guide": """插件开发指南：
1. 创建一个继承自FcsPluginInterface的Python类
2. 实现必要的方法：get_info(), get_ui_elements(), process_fcs()
3. 将插件打包为zip文件，包含所有必要的Python文件
4. 使用"安装新插件"功能安装

详细文档请参考项目GitHub页面。""",
            "view_github_doc": "查看GitHub文档",
            # 关于与支持
            "app_desc": """FCS细胞采样工具是一个用于处理流式细胞仪数据的应用程序。
        
它可以帮助您从大型FCS文件中提取样本，支持多种采样模式：
• 连续采样：从指定位置开始连续提取指定数量的细胞
• 间隔采样：按固定间隔从指定范围内提取细胞
• 随机采样：从指定范围内随机提取指定数量的细胞

本工具由cn111.net工作室开发，当前版本 {version}""",
            "donate_support": "打赏支持",
            "donate_intro": "如果您觉得这个工具对您有所帮助，欢迎扫描下方二维码进行打赏支持！",
            "wechat_pay": "微信支付",
            "alipay": "支付宝",
            "thank_you": "感谢您的支持，这将帮助我们持续改进和维护这个工具！",
            "update_info": "更新信息",
            "check_update_hint": '点击"检查更新"按钮查看是否有新版本可用。',
            "download_update": "下载更新",
            "view_release_notes": "查看发布说明",
            # 语言设置
            "language": "语言:",
            "lang_zh_CN": "中文",
            "lang_en_US": "English",
            "language_changed": "语言已更改，部分界面将在重启后完全更新",
            # 消息
            "error": "错误",
            "warning": "警告",
            "success": "成功",
            "info": "提示",
            "select_file_first": "请先选择FCS文件",
            "create_output_dir": "创建输出目录: {dir}",
            "cannot_create_dir": "无法创建输出目录: {error}",
            "use_temp_dir": "将使用临时目录: {dir}",
            "reading_file": "正在读取FCS文件...",
            "selected_file": "已选择文件: {file}",
            "total_cells": "文件中细胞总数: {count}",
            "output_dir_set": "输出目录已设置为: {dir}",
            "start_pos_range": "起始位置必须在0到{max}之间",
            "end_pos_range": "结束位置不能大于总细胞数{count}",
            "start_less_end": "起始位置必须小于结束位置",
            "start_sampling": "\n开始采样...",
            "sample_range": "采样范围: {start}-{end}",
            "sample_mode": "采样模式: {mode}",
            "sample_method": "采样方式: {desc}",
            "sampled_cells": "采样后细胞数: {count}",
            "apply_plugin": "\n应用插件: {name}",
            "plugin_error": "插件处理出错: {error}",
            "plugin_processed": "插件处理后细胞数: {count}",
            "saving_file": "\n正在保存文件...",
            "file_saved": "文件已保存: {file}",
            "sampling_complete": "采样完成！\n文件已保存到：\n{file}",
            "no_plugins": "暂无可用插件，请先安装插件",
            "no_ui_elements": "插件 '{name}' 未提供UI元素",
            "load_ui_error": "加载插件UI时出错: {error}",
            "select_plugin_to_uninstall": "请先选择要卸载的插件",
            "confirm_uninstall": "确定要卸载插件 '{name}' 吗？",
            "plugin_uninstalled": "插件 '{name}' 已卸载",
            "uninstall_failed": "卸载插件 '{name}' 失败",
            "uninstall_error": "卸载插件时出错: {error}",
            "select_plugin_file": "请先选择插件文件",
            "plugin_file_not_exist": "插件文件不存在",
            "plugin_installed": "插件安装成功",
            "install_failed": "插件安装失败",
            "install_error": "安装插件时出错: {error}",
            "checking_update": "检查中...",
            "update_available": "发现新版本 {version}！当前版本 {current}",
            "download_in_browser": "更新文件将在浏览器中下载。下载完成后，请关闭此应用程序并安装新版本。",
            "latest_version": "您的软件已是最新版本 {version}",
            "check_update_failed": "检查更新失败: {error}",
            "unsupported_mode": "不支持的采样模式",
            # 采样描述
            "continuous_desc": "连续采样前{count}个细胞",
            "interval_desc": "每{interval}个细胞采样1个",
            "random_desc": "随机采样{count}个细胞",
        }

    def _load_english(self):
        """加载英文翻译"""
        return {
            "app_title": "FCS Cell Sampling Tool",
            "check_update": "Check Update",
            "developed_by": "Developed by",
            "studio": "Studio",
            # Tab titles
            "tab_sampling": "Sampling",
            "tab_plugins": "Plugins",
            "tab_plugin_mgmt": "Plugin Management",
            "tab_about": "About & Support",
            # File settings
            "file_settings": "File Settings",
            "fcs_file": "FCS File:",
            "browse": "Browse...",
            "output_dir": "Output Directory:",
            # Sampling parameters
            "sampling_params": "Sampling Parameters",
            "start_pos": "Start Position:",
            "end_pos": "End Position:",
            "end_pos_hint": "(-1 means to the end of file)",
            "target_count": "Target Cell Count:",
            "target_count_hint": "(-1 means all)",
            "sample_mode": "Sampling Mode:",
            "continuous": "Continuous",
            "interval": "Interval",
            "random": "Random",
            # Buttons
            "start_sampling": "Start Sampling",
            "clear_info": "Clear Info",
            # Process info
            "process_info": "Process Information",
            # Plugin functionality
            "select_plugin": "Select Plugin",
            "available_plugins": "Available Plugins:",
            "load_plugin": "Load Plugin",
            "plugin_desc": "Plugin Description",
            "select_plugin_hint": "Please select a plugin to view description",
            "plugin_function": "Plugin Function",
            "load_plugin_hint": "Please select and load a plugin first",
            # Plugin management
            "installed_plugins": "Installed Plugins",
            "refresh_list": "Refresh List",
            "uninstall_plugin": "Uninstall Plugin",
            "install_new_plugin": "Install New Plugin",
            "plugin_file": "Plugin File:",
            "install_plugin": "Install Plugin",
            "plugin_dev": "Plugin Development",
            "plugin_dev_guide": """Plugin Development Guide:
1. Create a Python class that inherits from FcsPluginInterface
2. Implement required methods: get_info(), get_ui_elements(), process_fcs()
3. Package your plugin as a ZIP file with all necessary Python files
4. Use the "Install Plugin" feature to install

For detailed documentation, please refer to the project GitHub page.""",
            "view_github_doc": "View GitHub Docs",
            # About & Support
            "app_desc": """FCS Cell Sampling Tool is an application for processing flow cytometry data.
        
It helps you extract samples from large FCS files, supporting multiple sampling modes:
• Continuous: Extract a specified number of cells starting from a specified position
• Interval: Extract cells at fixed intervals from a specified range
• Random: Randomly extract a specified number of cells from a specified range

Developed by cn111.net Studio, current version {version}""",
            "donate_support": "Donate & Support",
            "donate_intro": "If you find this tool helpful, please consider scanning the QR codes below to donate!",
            "wechat_pay": "WeChat Pay",
            "alipay": "Alipay",
            "thank_you": "Thank you for your support, which will help us continue to improve and maintain this tool!",
            "update_info": "Update Information",
            "check_update_hint": 'Click the "Check Update" button to see if a new version is available.',
            "download_update": "Download Update",
            "view_release_notes": "View Release Notes",
            # Language settings
            "language": "Language:",
            "lang_zh_CN": "中文",
            "lang_en_US": "English",
            "language_changed": "Language changed, some UI elements will fully update after restart",
            # Messages
            "error": "Error",
            "warning": "Warning",
            "success": "Success",
            "info": "Information",
            "select_file_first": "Please select an FCS file first",
            "create_output_dir": "Created output directory: {dir}",
            "cannot_create_dir": "Cannot create output directory: {error}",
            "use_temp_dir": "Will use temporary directory: {dir}",
            "reading_file": "Reading FCS file...",
            "selected_file": "Selected file: {file}",
            "total_cells": "Total cells in file: {count}",
            "output_dir_set": "Output directory set to: {dir}",
            "start_pos_range": "Start position must be between 0 and {max}",
            "end_pos_range": "End position cannot be greater than total cell count {count}",
            "start_less_end": "Start position must be less than end position",
            "start_sampling": "\nStarting sampling...",
            "sample_range": "Sampling range: {start}-{end}",
            "sample_mode": "Sampling mode: {mode}",
            "sample_method": "Sampling method: {desc}",
            "sampled_cells": "Cells after sampling: {count}",
            "apply_plugin": "\nApplying plugin: {name}",
            "plugin_error": "Plugin processing error: {error}",
            "plugin_processed": "Cells after plugin processing: {count}",
            "saving_file": "\nSaving file...",
            "file_saved": "File saved: {file}",
            "sampling_complete": "Sampling complete!\nFile saved to:\n{file}",
            "no_plugins": "No plugins available, please install plugins first",
            "no_ui_elements": "Plugin '{name}' does not provide UI elements",
            "load_ui_error": "Error loading plugin UI: {error}",
            "select_plugin_to_uninstall": "Please select a plugin to uninstall",
            "confirm_uninstall": "Are you sure you want to uninstall plugin '{name}'?",
            "plugin_uninstalled": "Plugin '{name}' has been uninstalled",
            "uninstall_failed": "Failed to uninstall plugin '{name}'",
            "uninstall_error": "Error uninstalling plugin: {error}",
            "select_plugin_file": "Please select a plugin file first",
            "plugin_file_not_exist": "Plugin file does not exist",
            "plugin_installed": "Plugin installed successfully",
            "install_failed": "Plugin installation failed",
            "install_error": "Error installing plugin: {error}",
            "checking_update": "Checking...",
            "update_available": "New version {version} found! Current version {current}",
            "download_in_browser": "The update file will be downloaded in your browser. After downloading, please close this application and install the new version.",
            "latest_version": "Your software is already the latest version {version}",
            "check_update_failed": "Failed to check for updates: {error}",
            "unsupported_mode": "Unsupported sampling mode",
            # Sampling descriptions
            "continuous_desc": "Continuously sampled the first {count} cells",
            "interval_desc": "Sampled 1 cell every {interval} cells",
            "random_desc": "Randomly sampled {count} cells",
        }

    def set_language(self, lang_code):
        """设置当前语言"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False

    def get(self, key, **kwargs):
        """获取翻译文本"""
        if key in self.translations[self.current_lang]:
            text = self.translations[self.current_lang][key]
            # 处理格式化参数
            if kwargs:
                try:
                    return text.format(**kwargs)
                except:
                    return text
            return text
        # 如果找不到翻译，返回键名
        return key


# 创建全局翻译实例
i18n = I18n()


# 插件接口类
class FcsPluginInterface:
    """FCS处理插件接口，所有插件必须继承此类并实现必要的方法"""

    def __init__(self):
        self.name = "插件基类"
        self.description = "插件基类描述"
        self.version = "1.0.0"
        self.author = "未知"

    def get_info(self):
        """返回插件信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
        }

    def get_ui_elements(self, parent_frame):
        """返回插件的UI元素，将被添加到主界面的插件选项卡中

        Args:
            parent_frame: 父级框架，插件UI应该添加到这个框架中

        Returns:
            frame: 包含插件UI元素的框架
        """
        frame = ttk.Frame(parent_frame)
        ttk.Label(frame, text=f"插件 '{self.name}' UI").pack(pady=10)
        return frame

    def process_fcs(self, metadata, raw_data, params=None):
        """处理FCS数据

        Args:
            metadata: FCS文件元数据
            raw_data: FCS原始数据
            params: 处理参数字典

        Returns:
            tuple: (处理后的数据, 处理描述)
        """
        raise NotImplementedError("插件必须实现process_fcs方法")


# 插件管理器类
class PluginManager:
    """管理FCS处理插件的加载、卸载和执行"""

    def __init__(self):
        self.plugins = {}  # 存储已加载的插件
        self.plugin_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "plugins"
        )

        # 确保插件目录存在
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)

        # 将插件目录添加到Python路径
        if self.plugin_dir not in sys.path:
            sys.path.append(self.plugin_dir)

    def discover_plugins(self):
        """发现并加载所有可用的插件"""
        # 清空当前插件列表
        self.plugins = {}

        # 遍历插件目录中的所有Python文件
        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py") and not file.startswith("__"):
                try:
                    self._load_plugin_from_file(os.path.join(self.plugin_dir, file))
                except Exception as e:
                    print(f"加载插件 {file} 时出错: {str(e)}")

    def _load_plugin_from_file(self, file_path):
        """从文件加载插件

        Args:
            file_path: 插件文件路径
        """
        # 获取模块名（不含.py后缀）
        module_name = os.path.basename(file_path)[:-3]

        # 动态导入模块
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"无法从 {file_path} 加载模块")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 查找模块中继承自FcsPluginInterface的所有类
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, FcsPluginInterface)
                and obj is not FcsPluginInterface
            ):
                # 实例化插件并添加到插件列表
                plugin = obj()
                plugin_info = plugin.get_info()
                self.plugins[plugin_info["name"]] = plugin
                print(f"已加载插件: {plugin_info['name']} v{plugin_info['version']}")

    def install_plugin(self, zip_path):
        """安装新插件

        Args:
            zip_path: 插件zip文件路径

        Returns:
            bool: 安装是否成功
        """
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # 检查zip文件是否包含必要的文件
                file_list = zip_ref.namelist()
                py_files = [
                    f for f in file_list if f.endswith(".py") and not f.startswith("__")
                ]

                if not py_files:
                    raise ValueError("插件包中未找到Python文件")

                # 解压到插件目录
                zip_ref.extractall(self.plugin_dir)

            # 重新发现插件
            self.discover_plugins()
            return True
        except Exception as e:
            print(f"安装插件时出错: {str(e)}")
            return False

    def uninstall_plugin(self, plugin_name):
        """卸载插件

        Args:
            plugin_name: 要卸载的插件名称

        Returns:
            bool: 卸载是否成功
        """
        if plugin_name not in self.plugins:
            return False

        # 查找插件文件
        plugin_module = self.plugins[plugin_name].__class__.__module__
        plugin_file = f"{plugin_module}.py"
        plugin_path = os.path.join(self.plugin_dir, plugin_file)

        # 删除插件文件
        if os.path.exists(plugin_path):
            os.remove(plugin_path)

        # 从插件列表中移除
        del self.plugins[plugin_name]
        return True

    def get_plugin_list(self):
        """获取所有已加载插件的列表

        Returns:
            list: 插件信息字典列表
        """
        return [plugin.get_info() for plugin in self.plugins.values()]

    def get_plugin(self, name):
        """获取指定名称的插件

        Args:
            name: 插件名称

        Returns:
            FcsPluginInterface: 插件实例，如果不存在则返回None
        """
        return self.plugins.get(name)


class FcsSamplerGUI:
    def __init__(self, root):
        self.root = root
        # 使用翻译后的标题
        self.root.title(i18n.get("app_title"))
        self.root.geometry("700x850")
        self.root.configure(bg="#f5f5f5")

        # 初始化插件管理器
        self.plugin_manager = PluginManager()
        self.plugin_manager.discover_plugins()

        # 设置窗口大小调整时的行为
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 创建主框架
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 设置主框架的行列权重
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 创建标题和工作室信息框架
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # 添加标题
        title_label = ttk.Label(
            header_frame, text=i18n.get("app_title"), font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, sticky=tk.W)

        # 添加工作室信息和官网链接
        studio_frame = ttk.Frame(header_frame)
        studio_frame.grid(row=0, column=1, sticky=tk.E)

        # 添加语言选择
        lang_frame = ttk.Frame(studio_frame)
        lang_frame.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(lang_frame, text=i18n.get("language")).pack(side=tk.LEFT, padx=(0, 5))
        self.lang_var = tk.StringVar(value="zh_CN")  # 默认中文
        lang_combo = ttk.Combobox(
            lang_frame, textvariable=self.lang_var, state="readonly", width=6
        )
        lang_combo["values"] = ["zh_CN", "en_US"]
        lang_combo.pack(side=tk.LEFT)
        lang_combo.bind("<<ComboboxSelected>>", self._change_language)

        # 添加检查更新按钮
        self.update_button = ttk.Button(
            studio_frame, text=i18n.get("check_update"), command=self.check_for_updates
        )
        self.update_button.pack(side=tk.LEFT, padx=(0, 10))

        studio_label = ttk.Label(
            studio_frame, text=i18n.get("developed_by") + " ", font=("Arial", 10)
        )
        studio_label.pack(side=tk.LEFT)

        # 创建可点击的链接标签
        website_label = ttk.Label(
            studio_frame,
            text="cn111.net",
            foreground="blue",
            cursor="hand2",
            font=("Arial", 10, "underline"),
        )
        website_label.pack(side=tk.LEFT)
        website_label.bind(
            "<Button-1>", lambda e: self.open_website("http://cn111.net")
        )

        studio_label2 = ttk.Label(
            studio_frame, text=" " + i18n.get("studio"), font=("Arial", 10)
        )
        studio_label2.pack(side=tk.LEFT)

        # 设置列权重
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)

        # 创建内容区域的选项卡
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # 创建"采样"选项卡
        sampling_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(sampling_tab, text=i18n.get("tab_sampling"))

        # 设置采样选项卡的行列权重
        sampling_tab.grid_rowconfigure(3, weight=1)
        sampling_tab.grid_columnconfigure(0, weight=1)

        # 创建"关于"选项卡
        about_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(about_tab, text=i18n.get("tab_about"))

        # 设置关于选项卡的行列权重
        about_tab.grid_rowconfigure(0, weight=1)
        about_tab.grid_columnconfigure(0, weight=1)

        # 创建"插件"选项卡
        plugins_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(plugins_tab, text=i18n.get("tab_plugins"))

        # 设置插件选项卡的行列权重
        plugins_tab.grid_rowconfigure(0, weight=1)
        plugins_tab.grid_columnconfigure(0, weight=1)

        # 创建"插件管理"选项卡
        plugin_mgmt_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(plugin_mgmt_tab, text=i18n.get("tab_plugin_mgmt"))

        # 设置插件管理选项卡的行列权重
        plugin_mgmt_tab.grid_rowconfigure(0, weight=1)
        plugin_mgmt_tab.grid_columnconfigure(0, weight=1)

        # 初始化各选项卡内容
        self._init_sampling_tab(sampling_tab)
        self._init_about_tab(about_tab)
        self._init_plugins_tab(plugins_tab)
        self._init_plugin_mgmt_tab(plugin_mgmt_tab)

        # 设置样式
        self.setup_styles()

        # 绑定窗口大小调整事件
        self.root.bind("<Configure>", self.on_window_resize)

        # 自动检查更新（静默模式）
        self.latest_version = None
        self.release_url = None
        self.check_for_updates(silent=True)

    def _change_language(self, event):
        """切换语言"""
        new_lang = self.lang_var.get()
        if i18n.set_language(new_lang):
            # 更新UI文本
            self._update_ui_texts()
            messagebox.showinfo(i18n.get("info"), i18n.get("language_changed"))

    def _update_ui_texts(self):
        """更新UI上的所有文本为当前语言"""
        # 更新窗口标题
        self.root.title(i18n.get("app_title"))

        # 更新选项卡标题
        self.tab_control.tab(0, text=i18n.get("tab_sampling"))
        self.tab_control.tab(1, text=i18n.get("tab_about"))
        self.tab_control.tab(2, text=i18n.get("tab_plugins"))
        self.tab_control.tab(3, text=i18n.get("tab_plugin_mgmt"))

        # 更新按钮文本
        self.update_button.config(text=i18n.get("check_update"))

        # 更新更新信息区域
        if hasattr(self, "update_info"):
            self.update_info.config(text=i18n.get("check_update_hint"))

        if hasattr(self, "check_update_button"):
            self.check_update_button.config(text=i18n.get("check_update"))

        if hasattr(self, "download_button"):
            self.download_button.config(text=i18n.get("download_update"))

        if hasattr(self, "release_notes_button"):
            self.release_notes_button.config(text=i18n.get("view_release_notes"))

    def _init_sampling_tab(self, tab):
        """初始化采样选项卡内容"""
        # 文件选择部分
        file_section = ttk.LabelFrame(tab, text=i18n.get("file_settings"), padding=10)
        file_section.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_section.columnconfigure(1, weight=1)

        # 文件选择
        ttk.Label(file_section, text=i18n.get("fcs_file")).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_section, textvariable=self.file_path, width=50)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        file_button = ttk.Button(
            file_section, text=i18n.get("browse"), command=self.select_file
        )
        file_button.grid(row=0, column=2, padx=(5, 0))

        # 输出目录选择
        ttk.Label(file_section, text=i18n.get("output_dir")).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0)
        )
        self.output_dir = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        output_entry = ttk.Entry(file_section, textvariable=self.output_dir, width=50)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=(10, 0))
        output_button = ttk.Button(
            file_section, text=i18n.get("browse"), command=self.select_output_dir
        )
        output_button.grid(row=1, column=2, padx=(5, 0), pady=(10, 0))

        # 参数设置部分
        param_section = ttk.LabelFrame(
            tab, text=i18n.get("sampling_params"), padding=10
        )
        param_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        param_section.columnconfigure(1, weight=1)

        # 范围设置
        ttk.Label(param_section, text=i18n.get("start_pos")).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        self.range_start = tk.StringVar(value="0")
        ttk.Entry(param_section, textvariable=self.range_start, width=10).grid(
            row=0, column=1, sticky=tk.W, padx=5
        )

        ttk.Label(param_section, text=i18n.get("end_pos")).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0)
        )
        self.range_end = tk.StringVar(value="-1")
        ttk.Entry(param_section, textvariable=self.range_end, width=10).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=(10, 0)
        )
        ttk.Label(param_section, text=i18n.get("end_pos_hint")).grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=(10, 0)
        )

        ttk.Label(param_section, text=i18n.get("target_count")).grid(
            row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0)
        )
        self.target_count = tk.StringVar(value="1000")
        ttk.Entry(param_section, textvariable=self.target_count, width=10).grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=(10, 0)
        )
        ttk.Label(param_section, text=i18n.get("target_count_hint")).grid(
            row=2, column=2, sticky=tk.W, padx=5, pady=(10, 0)
        )

        # 采样模式
        ttk.Label(param_section, text=i18n.get("sample_mode")).grid(
            row=3, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0)
        )
        self.sample_mode = tk.StringVar(value="continuous")
        mode_frame = ttk.Frame(param_section)
        mode_frame.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=(10, 0))

        ttk.Radiobutton(
            mode_frame,
            text=i18n.get("continuous"),
            variable=self.sample_mode,
            value="continuous",
        ).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(
            mode_frame,
            text=i18n.get("interval"),
            variable=self.sample_mode,
            value="interval",
        ).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(
            mode_frame,
            text=i18n.get("random"),
            variable=self.sample_mode,
            value="random",
        ).pack(side=tk.LEFT)

        # 按钮部分
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        button_frame.columnconfigure(0, weight=1)  # 使按钮居中

        # 使用ttk.Button替代自定义按钮，保持与应用整体风格一致
        start_button = ttk.Button(
            button_frame,
            text=i18n.get("start_sampling"),
            command=self.start_sampling,
            style="TButton",
            width=20  # 增加按钮宽度从15到20
        )
        # 使用grid而不是pack，更好地控制按钮位置
        start_button.grid(row=0, column=0, pady=15)  # 增加上下内边距从10到15

        # 信息显示部分
        info_section = ttk.LabelFrame(tab, text=i18n.get("process_info"), padding=10)
        info_section.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        info_section.columnconfigure(0, weight=1)  # 信息文本框可以水平扩展
        info_section.rowconfigure(0, weight=1)  # 信息文本框可以垂直扩展

        # 创建带滚动条的文本框
        info_frame = ttk.Frame(info_section)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)

        self.info_text = tk.Text(info_frame, wrap=tk.WORD, width=60, height=10)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(
            info_frame, orient=tk.VERTICAL, command=self.info_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text["yscrollcommand"] = scrollbar.set

        # 添加清除按钮
        clear_button = ttk.Button(
            info_section, text=i18n.get("clear_info"), command=self.clear_info
        )
        clear_button.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))

    def _init_about_tab(self, tab):
        """初始化关于选项卡内容"""
        # 使用直接的布局方式，不使用Canvas
        about_content = ttk.Frame(tab)
        about_content.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10
        )

        # 设置关于内容的列权重
        about_content.columnconfigure(0, weight=1)

        # 应用程序描述
        desc_frame = ttk.Frame(about_content)
        desc_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        desc_frame.columnconfigure(0, weight=1)

        # 获取当前版本
        self.current_version = self.get_current_version()

        desc_text = i18n.get("app_desc", version=self.current_version)

        desc_label = ttk.Label(
            desc_frame, text=desc_text, wraplength=600, justify=tk.LEFT
        )
        desc_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # 打赏二维码部分
        donate_frame = ttk.LabelFrame(
            about_content, text=i18n.get("donate_support"), padding=10
        )
        donate_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        # 设置打赏框架的列权重
        donate_frame.columnconfigure(0, weight=1)

        # 添加说明文字
        intro_text = i18n.get("donate_intro")
        ttk.Label(donate_frame, text=intro_text, wraplength=600).grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # 创建二维码容器框架
        qrcode_container = ttk.Frame(donate_frame)
        qrcode_container.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # 设置二维码容器的列权重，使二维码居中
        qrcode_container.columnconfigure(0, weight=1)
        qrcode_container.columnconfigure(1, weight=1)
        qrcode_container.columnconfigure(2, weight=1)

        # 加载并显示微信二维码
        try:
            wechat_img = Image.open("qrcode-wechat-small.png")  # 使用PNG格式
            # 保持原始比例，只指定宽度，高度自动计算
            width = 150
            wpercent = width / float(wechat_img.size[0])
            hsize = int((float(wechat_img.size[1]) * float(wpercent)))
            wechat_img = wechat_img.resize((width, hsize), Image.LANCZOS)
            self.wechat_photo = ImageTk.PhotoImage(wechat_img)

            # 创建微信支付框架
            wechat_frame = ttk.Frame(qrcode_container)
            wechat_frame.grid(row=0, column=0, padx=20, pady=5, sticky=tk.E)

            # 添加微信二维码和标签
            wechat_label = ttk.Label(wechat_frame, image=self.wechat_photo)
            wechat_label.pack(pady=5)
            ttk.Label(wechat_frame, text="微信支付", font=("Arial", 10, "bold")).pack()
        except Exception as e:
            print(f"加载微信二维码出错: {e}")

        # 加载并显示支付宝二维码
        try:
            alipay_img = Image.open("qrcode-alipay-small.png")  # 使用PNG格式
            # 保持原始比例，只指定宽度，高度自动计算
            width = 150
            wpercent = width / float(alipay_img.size[0])
            hsize = int((float(alipay_img.size[1]) * float(wpercent)))
            alipay_img = alipay_img.resize((width, hsize), Image.LANCZOS)
            self.alipay_photo = ImageTk.PhotoImage(alipay_img)

            # 创建支付宝框架
            alipay_frame = ttk.Frame(qrcode_container)
            alipay_frame.grid(row=0, column=2, padx=20, pady=5, sticky=tk.W)

            # 添加支付宝二维码和标签
            alipay_label = ttk.Label(alipay_frame, image=self.alipay_photo)
            alipay_label.pack(pady=5)
            ttk.Label(alipay_frame, text="支付宝", font=("Arial", 10, "bold")).pack()
        except Exception as e:
            print(f"加载支付宝二维码出错: {e}")

        # 添加感谢文字
        thank_text = "感谢您的支持，这将帮助我们持续改进和维护这个工具！"
        ttk.Label(
            donate_frame, text=thank_text, wraplength=600, font=("Arial", 10, "italic")
        ).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        # 添加更新信息区域
        self.update_frame = ttk.LabelFrame(about_content, text="更新信息", padding=10)
        self.update_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        self.update_frame.columnconfigure(0, weight=1)

        self.update_info = ttk.Label(
            self.update_frame,
            text='点击"检查更新"按钮查看是否有新版本可用。',
            wraplength=600,
        )
        self.update_info.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        self.update_action_frame = ttk.Frame(self.update_frame)
        self.update_action_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.check_update_button = ttk.Button(
            self.update_action_frame,
            text="检查更新",
            command=lambda: self.check_for_updates(False),
        )
        self.check_update_button.pack(side=tk.LEFT, padx=5)

        self.download_button = ttk.Button(
            self.update_action_frame,
            text="下载更新",
            command=self.download_update,
            state=tk.DISABLED,
        )
        self.download_button.pack(side=tk.LEFT, padx=5)

        self.release_notes_button = ttk.Button(
            self.update_action_frame,
            text="查看发布说明",
            command=self.view_release_notes,
            state=tk.DISABLED,
        )
        self.release_notes_button.pack(side=tk.LEFT, padx=5)

    def get_current_version(self):
        """获取当前版本号"""
        try:
            with open("version.txt", "r") as f:
                return f.read().strip()
        except:
            return "1.0.0"  # 默认版本号

    def check_for_updates(self, silent=False):
        """检查更新"""
        # 禁用更新按钮，避免重复点击
        self.update_button.configure(state=tk.DISABLED, text="检查中...")

        # 在后台线程中执行网络请求
        threading.Thread(
            target=self._check_updates_thread, args=(silent,), daemon=True
        ).start()

    def _check_updates_thread(self, silent):
        """在后台线程中检查更新"""
        try:
            # 获取GitHub仓库的最新发布信息
            response = requests.get(
                "https://api.github.com/repos/fastnas2023/fcs-sampler-test/releases/latest",
                timeout=10,
            )

            if response.status_code == 200:
                release_info = response.json()
                self.latest_version = release_info.get("tag_name", "").lstrip("v")
                self.release_url = release_info.get("html_url")
                self.release_notes = release_info.get("body", "")

                # 获取下载链接
                assets = release_info.get("assets", [])
                for asset in assets:
                    if self._is_suitable_download(asset.get("name", "")):
                        self.download_url = asset.get("browser_download_url")
                        break

                # 在主线程中更新UI
                self.root.after(0, lambda: self._update_ui_after_check(silent))
            else:
                # 在主线程中显示错误
                self.root.after(
                    0,
                    lambda: self._show_update_error(
                        "无法获取更新信息，服务器返回错误。", silent
                    ),
                )

        except Exception as e:
            # 在主线程中显示错误
            self.root.after(
                0, lambda: self._show_update_error(f"检查更新时出错: {str(e)}", silent)
            )

    def _is_suitable_download(self, filename):
        """判断文件是否适合当前系统"""
        import platform

        system = platform.system().lower()

        if system == "windows" and (
            filename.endswith(".exe") or filename.endswith(".msi")
        ):
            return True
        elif system == "darwin" and (
            filename.endswith(".dmg") or filename.endswith(".pkg")
        ):
            return True
        elif system == "linux" and (
            filename.endswith(".deb")
            or filename.endswith(".rpm")
            or filename.endswith(".AppImage")
        ):
            return True

        return False

    def _update_ui_after_check(self, silent):
        """更新检查完成后更新UI"""
        # 恢复更新按钮
        self.update_button.configure(state=tk.NORMAL, text="检查更新")

        if self._is_newer_version(self.latest_version, self.current_version):
            # 有新版本可用
            self.update_info.configure(
                text=f"发现新版本 {self.latest_version}！当前版本 {self.current_version}"
            )

            # 启用下载和查看发布说明按钮
            if self.download_url:
                self.download_button.configure(state=tk.NORMAL)

            if self.release_url:
                self.release_notes_button.configure(state=tk.NORMAL)

            # 如果不是静默检查，显示提示
            if not silent:
                messagebox.showinfo(
                    "更新可用",
                    f"发现新版本 {self.latest_version}！\n您可以在'关于与支持'选项卡中下载更新。",
                )

        else:
            # 已是最新版本
            self.update_info.configure(
                text=f"您的软件已是最新版本 {self.current_version}"
            )

            # 禁用下载和查看发布说明按钮
            self.download_button.configure(state=tk.DISABLED)
            self.release_notes_button.configure(state=tk.DISABLED)

            # 如果不是静默检查，显示提示
            if not silent:
                messagebox.showinfo(
                    "已是最新版本", f"您的软件已是最新版本 {self.current_version}"
                )

    def _show_update_error(self, error_message, silent):
        """显示更新错误"""
        # 恢复更新按钮
        self.update_button.configure(state=tk.NORMAL, text="检查更新")

        # 更新信息
        self.update_info.configure(text=f"检查更新失败: {error_message}")

        # 如果不是静默检查，显示错误
        if not silent:
            messagebox.showerror("检查更新失败", error_message)

    def _is_newer_version(self, version1, version2):
        """比较版本号，如果version1比version2新，返回True"""

        def normalize(v):
            # 移除前缀v（如果有）
            v = v.lstrip("v")
            # 将版本号分割为数字部分
            parts = re.findall(r"\d+", v)
            # 转换为整数列表
            return [int(x) for x in parts]

        v1 = normalize(version1 or "")
        v2 = normalize(version2 or "")

        # 比较版本号
        return v1 > v2

    def download_update(self):
        """下载更新"""
        if self.download_url:
            webbrowser.open_new(self.download_url)
            messagebox.showinfo(
                "下载已开始",
                "更新文件将在浏览器中下载。下载完成后，请关闭此应用程序并安装新版本。",
            )

    def view_release_notes(self):
        """查看发布说明"""
        if self.release_url:
            webbrowser.open_new(self.release_url)

    def on_window_resize(self, event):
        """处理窗口大小变化事件"""
        # 只处理来自根窗口的事件
        if event.widget == self.root:
            # 可以在这里添加额外的调整逻辑
            pass

    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()

        # 设置按钮样式 - 优化中文显示
        style.configure(
            "Accent.TButton", 
            font=("Microsoft YaHei", 12, "bold"),  # 使用更适合中文显示的字体
            padding=(20, 10),  # 增加内边距，水平20像素，垂直10像素
            background="#4CAF50",  # 设置背景色
            foreground="#ffffff",  # 设置文字颜色
            anchor="center"  # 确保文本居中
        )
        
        # 设置标准按钮样式
        style.configure(
            "TButton",
            font=("Microsoft YaHei", 11, "bold"),  # 设置字体
            padding=(15, 8)  # 设置内边距
        )
        
        # 设置按钮鼠标悬停样式
        style.map(
            "Accent.TButton",
            background=[("active", "#45a049")],  # 鼠标悬停时的背景色
            foreground=[("active", "#ffffff")]  # 鼠标悬停时的文字颜色
        )

        # 设置标签框架样式
        style.configure("TLabelframe", borderwidth=2)
        style.configure("TLabelframe.Label", font=("Microsoft YaHei", 11, "bold"))

        # 设置选项卡样式
        style.configure("TNotebook", tabposition="n")
        style.configure("TNotebook.Tab", font=("Microsoft YaHei", 10), padding=[10, 2])

    def open_website(self, url):
        """打开网站链接"""
        webbrowser.open_new(url)

    def select_file(self):
        filename = filedialog.askopenfilename(
            title="选择FCS文件",
            filetypes=[("FCS files", "*.fcs"), ("All files", "*.*")],
        )
        if filename:
            self.file_path.set(filename)
            # 读取文件获取细胞总数
            try:
                metadata, raw_data = parse(filename)
                total_cells = len(raw_data)
                self.show_info(f"已选择文件: {filename}")
                self.show_info(f"文件中细胞总数: {total_cells}")
                # 更新结束位置和目标数量为总细胞数
                self.range_end.set(str(total_cells))
                self.target_count.set(str(total_cells))
            except Exception as e:
                self.show_info(f"读取文件出错: {str(e)}")

    def select_output_dir(self):
        directory = filedialog.askdirectory(
            title="选择输出目录", initialdir=self.output_dir.get()
        )
        if directory:
            self.output_dir.set(directory)
            self.show_info(f"输出目录已设置为: {directory}")

    def show_info(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)

    def clear_info(self):
        self.info_text.delete(1.0, tk.END)

    def start_sampling(self):
        try:
            # 获取参数
            source_file = self.file_path.get()
            if not source_file:
                messagebox.showerror("错误", "请先选择FCS文件")
                return

            # 检查输出目录
            output_dir = self.output_dir.get()
            if not os.path.isdir(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    self.show_info(f"创建输出目录: {output_dir}")
                except Exception as e:
                    self.show_info(f"无法创建输出目录: {str(e)}")
                    # 如果无法创建目录，使用临时目录
                    output_dir = tempfile.gettempdir()
                    self.show_info(f"将使用临时目录: {output_dir}")

            # 读取文件
            self.show_info("正在读取FCS文件...")
            metadata, raw_data = parse(source_file)
            total_cells = len(raw_data)

            # 处理参数
            range_start = int(self.range_start.get())
            range_end = int(self.range_end.get())
            target_count = int(self.target_count.get())

            # 处理特殊值
            if range_end == -1:
                range_end = total_cells
            if target_count == -1:
                target_count = total_cells

            sample_mode = self.sample_mode.get()

            # 验证参数
            if range_start < 0 or range_start >= total_cells:
                raise ValueError(f"起始位置必须在0到{total_cells-1}之间")
            if range_end > total_cells:
                raise ValueError(f"结束位置不能大于总细胞数{total_cells}")
            if range_start >= range_end:
                raise ValueError("起始位置必须小于结束位置")

            # 执行采样
            self.show_info("\n开始采样...")
            sampled_cells, sample_desc = sample_cells(
                raw_data, range_start, range_end, target_count, sample_mode
            )

            # 显示采样结果
            self.show_info(f"采样范围: {range_start}-{range_end}")
            self.show_info(f"采样模式: {sample_mode}")
            self.show_info(f"采样方式: {sample_desc}")
            self.show_info(f"采样后细胞数: {len(sampled_cells)}")

            # 应用插件处理（如果有选择插件）
            selected_plugin = (
                self.selected_plugin.get() if hasattr(self, "selected_plugin") else None
            )
            if selected_plugin and selected_plugin != "暂无可用插件":
                plugin = self.plugin_manager.get_plugin(selected_plugin)
                if plugin:
                    self.show_info(f"\n应用插件: {selected_plugin}")
                    try:
                        # 调用插件处理数据
                        processed_data, process_desc = plugin.process_fcs(
                            metadata, sampled_cells
                        )
                        self.show_info(process_desc)

                        # 更新采样结果
                        if processed_data is not None and len(processed_data) > 0:
                            sampled_cells = processed_data
                            self.show_info(f"插件处理后细胞数: {len(sampled_cells)}")
                    except Exception as e:
                        self.show_info(f"插件处理出错: {str(e)}")

            # 准备输出数据
            cell_data = sampled_cells.values.flatten()
            if not np.issubdtype(cell_data.dtype, np.floating):
                cell_data = cell_data.astype(np.float32)

            # 更新元数据
            output_metadata = metadata.copy()
            output_metadata["$TOT"] = len(sampled_cells)

            # 生成输出文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = (
                f"sampled_{range_start}-{range_end}_mode{sample_mode}_{timestamp}.fcs"
            )
            output_file = os.path.join(output_dir, output_filename)

            # 写入新文件
            self.show_info("\n正在保存文件...")
            with open(output_file, "wb") as f:
                flow_data = flowio.create_fcs(
                    f,
                    event_data=cell_data,
                    channel_names=[
                        metadata[f"$P{i}N"] for i in range(1, metadata["$PAR"] + 1)
                    ],
                )

            self.show_info(f"文件已保存: {output_file}")
            messagebox.showinfo("成功", f"采样完成！\n文件已保存到：\n{output_file}")

        except Exception as e:
            self.show_info(f"\n错误: {str(e)}")
            messagebox.showerror("错误", str(e))

    def _init_plugins_tab(self, tab):
        """初始化插件功能选项卡内容"""
        # 创建插件内容框架
        plugins_content = ttk.Frame(tab)
        plugins_content.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10
        )
        plugins_content.columnconfigure(0, weight=1)

        # 插件选择部分
        plugin_select_frame = ttk.LabelFrame(
            plugins_content, text="选择插件", padding=10
        )
        plugin_select_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        plugin_select_frame.columnconfigure(0, weight=1)

        # 创建插件选择下拉框
        ttk.Label(plugin_select_frame, text="可用插件:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )

        self.selected_plugin = tk.StringVar()
        self.plugin_combobox = ttk.Combobox(
            plugin_select_frame, textvariable=self.selected_plugin, state="readonly"
        )
        self.plugin_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # 加载插件按钮
        load_button = ttk.Button(
            plugin_select_frame, text="加载插件", command=self._load_selected_plugin
        )
        load_button.grid(row=0, column=2, padx=(5, 0))

        # 插件描述部分
        self.plugin_desc_frame = ttk.LabelFrame(
            plugins_content, text="插件描述", padding=10
        )
        self.plugin_desc_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        self.plugin_desc_frame.columnconfigure(0, weight=1)

        self.plugin_desc_label = ttk.Label(
            self.plugin_desc_frame, text="请选择一个插件以查看描述", wraplength=600
        )
        self.plugin_desc_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        # 插件UI部分
        self.plugin_ui_frame = ttk.LabelFrame(
            plugins_content, text="插件功能", padding=10
        )
        self.plugin_ui_frame.grid(
            row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0)
        )
        self.plugin_ui_frame.columnconfigure(0, weight=1)
        self.plugin_ui_frame.rowconfigure(0, weight=1)

        self.plugin_ui_placeholder = ttk.Label(
            self.plugin_ui_frame, text="请先选择并加载一个插件", wraplength=600
        )
        self.plugin_ui_placeholder.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=20)

        # 更新插件列表
        self._update_plugin_list()

        # 绑定选择事件
        self.plugin_combobox.bind("<<ComboboxSelected>>", self._on_plugin_selected)

    def _init_plugin_mgmt_tab(self, tab):
        """初始化插件管理选项卡内容"""
        # 创建插件管理内容框架
        mgmt_content = ttk.Frame(tab)
        mgmt_content.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10
        )
        mgmt_content.columnconfigure(0, weight=1)

        # 已安装插件部分
        installed_frame = ttk.LabelFrame(mgmt_content, text="已安装插件", padding=10)
        installed_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        installed_frame.columnconfigure(0, weight=1)

        # 创建插件列表框
        self.plugin_listbox = tk.Listbox(installed_frame, height=6)
        self.plugin_listbox.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5)
        )

        # 添加滚动条
        plugin_scrollbar = ttk.Scrollbar(
            installed_frame, orient=tk.VERTICAL, command=self.plugin_listbox.yview
        )
        plugin_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.plugin_listbox["yscrollcommand"] = plugin_scrollbar.set

        # 插件操作按钮
        plugin_actions = ttk.Frame(installed_frame)
        plugin_actions.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0)
        )

        refresh_button = ttk.Button(
            plugin_actions, text="刷新列表", command=self._refresh_plugin_list
        )
        refresh_button.pack(side=tk.LEFT, padx=(0, 5))

        uninstall_button = ttk.Button(
            plugin_actions, text="卸载插件", command=self._uninstall_selected_plugin
        )
        uninstall_button.pack(side=tk.LEFT, padx=5)

        # 安装新插件部分
        install_frame = ttk.LabelFrame(mgmt_content, text="安装新插件", padding=10)
        install_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        install_frame.columnconfigure(1, weight=1)

        ttk.Label(install_frame, text="插件文件:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )

        self.plugin_file_path = tk.StringVar()
        plugin_file_entry = ttk.Entry(
            install_frame, textvariable=self.plugin_file_path, width=50
        )
        plugin_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        plugin_file_button = ttk.Button(
            install_frame, text="浏览...", command=self._select_plugin_file
        )
        plugin_file_button.grid(row=0, column=2, padx=(5, 0))

        install_button = ttk.Button(
            install_frame, text="安装插件", command=self._install_plugin
        )
        install_button.grid(row=1, column=1, sticky=tk.E, pady=(10, 0))

        # 插件开发指南部分
        dev_frame = ttk.LabelFrame(mgmt_content, text="插件开发", padding=10)
        dev_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        dev_frame.columnconfigure(0, weight=1)

        dev_text = """插件开发指南：
1. 创建一个继承自FcsPluginInterface的Python类
2. 实现必要的方法：get_info(), get_ui_elements(), process_fcs()
3. 将插件打包为zip文件，包含所有必要的Python文件
4. 使用"安装新插件"功能安装

详细文档请参考项目GitHub页面。"""

        dev_label = ttk.Label(dev_frame, text=dev_text, wraplength=600, justify=tk.LEFT)
        dev_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        github_button = ttk.Button(
            dev_frame,
            text="查看GitHub文档",
            command=lambda: self.open_website(
                "https://github.com/fastnas2023/fcs-sampler-test"
            ),
        )
        github_button.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))

        # 初始化插件列表
        self._refresh_plugin_list()

    def _update_plugin_list(self):
        """更新插件下拉列表"""
        plugin_list = self.plugin_manager.get_plugin_list()
        plugin_names = [p["name"] for p in plugin_list]

        if plugin_names:
            self.plugin_combobox["values"] = plugin_names
            self.plugin_combobox.current(0)  # 选择第一个插件
            self._on_plugin_selected(None)  # 触发选择事件
        else:
            self.plugin_combobox["values"] = ["暂无可用插件"]
            self.plugin_combobox.current(0)
            self.plugin_desc_label.config(text="未找到任何插件。请先安装插件。")

    def _on_plugin_selected(self, event):
        """处理插件选择事件"""
        selected = self.selected_plugin.get()
        if selected == "暂无可用插件":
            return

        plugin = self.plugin_manager.get_plugin(selected)
        if plugin:
            info = plugin.get_info()
            desc_text = f"""名称: {info['name']}
版本: {info['version']}
作者: {info['author']}

描述: {info['description']}"""
            self.plugin_desc_label.config(text=desc_text)

    def _load_selected_plugin(self):
        """加载选中的插件"""
        selected = self.selected_plugin.get()
        if selected == "暂无可用插件":
            messagebox.showinfo("提示", "暂无可用插件，请先安装插件")
            return

        plugin = self.plugin_manager.get_plugin(selected)
        if plugin:
            # 清空插件UI框架
            for widget in self.plugin_ui_frame.winfo_children():
                widget.destroy()

            # 获取插件UI元素
            try:
                plugin_ui = plugin.get_ui_elements(self.plugin_ui_frame)
                if plugin_ui:
                    plugin_ui.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                else:
                    ttk.Label(
                        self.plugin_ui_frame,
                        text=f"插件 '{selected}' 未提供UI元素",
                        wraplength=600,
                    ).pack(pady=20)
            except Exception as e:
                ttk.Label(
                    self.plugin_ui_frame,
                    text=f"加载插件UI时出错: {str(e)}",
                    wraplength=600,
                ).pack(pady=20)

    def _refresh_plugin_list(self):
        """刷新插件列表"""
        # 重新发现插件
        self.plugin_manager.discover_plugins()

        # 更新插件下拉列表
        self._update_plugin_list()

        # 更新插件列表框
        self.plugin_listbox.delete(0, tk.END)
        for plugin_info in self.plugin_manager.get_plugin_list():
            self.plugin_listbox.insert(
                tk.END, f"{plugin_info['name']} (v{plugin_info['version']})"
            )

    def _select_plugin_file(self):
        """选择插件文件"""
        file_path = filedialog.askopenfilename(
            title="选择插件文件", filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if file_path:
            self.plugin_file_path.set(file_path)

    def _install_plugin(self):
        """安装插件"""
        file_path = self.plugin_file_path.get()
        if not file_path:
            messagebox.showwarning("警告", "请先选择插件文件")
            return

        if not os.path.exists(file_path):
            messagebox.showerror("错误", "插件文件不存在")
            return

        try:
            success = self.plugin_manager.install_plugin(file_path)
            if success:
                messagebox.showinfo("成功", "插件安装成功")
                self._refresh_plugin_list()
            else:
                messagebox.showerror("错误", "插件安装失败")
        except Exception as e:
            messagebox.showerror("错误", f"安装插件时出错: {str(e)}")

    def _uninstall_selected_plugin(self):
        """卸载选中的插件"""
        selected_idx = self.plugin_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("警告", "请先选择要卸载的插件")
            return

        # 获取插件名称（去除版本信息）
        plugin_text = self.plugin_listbox.get(selected_idx[0])
        plugin_name = plugin_text.split(" (v")[0]

        # 确认卸载
        confirm = messagebox.askyesno("确认", f"确定要卸载插件 '{plugin_name}' 吗？")
        if not confirm:
            return

        try:
            success = self.plugin_manager.uninstall_plugin(plugin_name)
            if success:
                messagebox.showinfo("成功", f"插件 '{plugin_name}' 已卸载")
                self._refresh_plugin_list()
            else:
                messagebox.showerror("错误", f"卸载插件 '{plugin_name}' 失败")
        except Exception as e:
            messagebox.showerror("错误", f"卸载插件时出错: {str(e)}")


def sample_cells(raw_data, range_start, range_end, target_count, mode="continuous"):
    """
    细胞采样函数
    mode: 采样模式 - 'continuous'（连续）, 'interval'（间隔）, 'random'（随机）
    """
    cells_in_range = raw_data.iloc[range_start:range_end]
    range_count = len(cells_in_range)

    if mode == "continuous":
        # 连续采样：直接取前target_count个细胞
        sampled_cells = cells_in_range.iloc[:target_count]
        sample_desc = f"连续采样前{target_count}个细胞"

    elif mode == "interval":
        # 间隔采样：计算所需间隔
        interval = range_count // target_count
        if interval < 1:
            interval = 1
        sampled_cells = cells_in_range.iloc[::interval]
        sample_desc = f"每{interval}个细胞采样1个"

    elif mode == "random":
        # 随机采样：随机选择target_count个细胞
        sample_size = min(target_count, range_count)
        random_indices = np.random.choice(range_count, sample_size, replace=False)
        random_indices.sort()  # 排序以保持细胞顺序
        sampled_cells = cells_in_range.iloc[random_indices]
        sample_desc = f"随机采样{sample_size}个细胞"

    else:
        raise ValueError("不支持的采样模式")

    return sampled_cells, sample_desc


def main():
    """
    应用程序入口点，用于Windows安装程序
    """
    root = tk.Tk()
    app = FcsSamplerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
