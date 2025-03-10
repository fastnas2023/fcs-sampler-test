"""
FCS门控插件 - 用于对FCS数据进行门控分析
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 导入插件接口
from fcs_sampler_gui import FcsPluginInterface

class FcsGatingPlugin(FcsPluginInterface):
    """FCS门控插件，用于对FCS数据进行门控分析"""
    
    def __init__(self):
        super().__init__()
        self.name = "FCS门控插件"
        self.description = "对FCS数据进行门控分析，可以根据指定参数筛选细胞"
        self.version = "1.0.0"
        self.author = "FCS工具开发团队"
        
        # 插件UI元素
        self.ui_frame = None
        self.param1_var = None
        self.param2_var = None
        self.min_var = None
        self.max_var = None
        self.canvas = None
        self.fig = None
        
        # 数据
        self.metadata = None
        self.raw_data = None
        self.param_names = []
    
    def get_ui_elements(self, parent_frame):
        """创建插件UI元素"""
        self.ui_frame = ttk.Frame(parent_frame)
        
        # 参数选择部分
        param_frame = ttk.LabelFrame(self.ui_frame, text="门控参数", padding=10)
        param_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 参数1选择
        ttk.Label(param_frame, text="参数1:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.param1_var = tk.StringVar()
        self.param1_combo = ttk.Combobox(param_frame, textvariable=self.param1_var, state="readonly")
        self.param1_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # 参数2选择
        ttk.Label(param_frame, text="参数2:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.param2_var = tk.StringVar()
        self.param2_combo = ttk.Combobox(param_frame, textvariable=self.param2_var, state="readonly")
        self.param2_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=(10, 0))
        
        # 门控范围
        gate_frame = ttk.LabelFrame(self.ui_frame, text="门控范围", padding=10)
        gate_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 最小值
        ttk.Label(gate_frame, text="最小值:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.min_var = tk.StringVar(value="0")
        ttk.Entry(gate_frame, textvariable=self.min_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 最大值
        ttk.Label(gate_frame, text="最大值:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.max_var = tk.StringVar(value="1000")
        ttk.Entry(gate_frame, textvariable=self.max_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=(10, 0))
        
        # 操作按钮
        button_frame = ttk.Frame(self.ui_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="加载数据", command=self._load_data)
        load_button.pack(side=tk.LEFT, padx=5)
        
        plot_button = ttk.Button(button_frame, text="绘制散点图", command=self._plot_data)
        plot_button.pack(side=tk.LEFT, padx=5)
        
        gate_button = ttk.Button(button_frame, text="应用门控", command=self._apply_gate)
        gate_button.pack(side=tk.LEFT, padx=5)
        
        # 图表区域
        plot_frame = ttk.LabelFrame(self.ui_frame, text="数据可视化", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建matplotlib图形
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 初始状态提示
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, "请先加载FCS数据", ha='center', va='center', fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
        
        return self.ui_frame
    
    def process_fcs(self, metadata, raw_data, params=None):
        """处理FCS数据
        
        Args:
            metadata: FCS文件元数据
            raw_data: FCS原始数据
            params: 处理参数字典
            
        Returns:
            tuple: (处理后的数据, 处理描述)
        """
        # 保存数据
        self.metadata = metadata
        self.raw_data = raw_data
        
        # 获取参数名称
        self.param_names = [metadata[f'$P{i}N'] for i in range(1, metadata['$PAR']+1)]
        
        # 更新UI
        if self.param1_combo:
            self.param1_combo["values"] = self.param_names
            self.param2_combo["values"] = self.param_names
            
            if len(self.param_names) > 0:
                self.param1_combo.current(0)
            if len(self.param_names) > 1:
                self.param2_combo.current(1)
        
        # 如果提供了参数，执行门控
        if params and 'param1' in params and 'param2' in params:
            return self._gate_data(params['param1'], params['param2'], 
                                  float(params.get('min', 0)), 
                                  float(params.get('max', 1000)))
        
        return raw_data, "数据已加载，未应用门控"
    
    def _load_data(self):
        """加载数据按钮回调"""
        if self.raw_data is None:
            tk.messagebox.showinfo("提示", "请先在主界面加载FCS文件，然后点击'加载插件'按钮")
            return
            
        # 更新UI
        tk.messagebox.showinfo("成功", f"已加载FCS数据，共{len(self.raw_data)}个细胞，{len(self.param_names)}个参数")
    
    def _plot_data(self):
        """绘制散点图按钮回调"""
        if self.raw_data is None:
            tk.messagebox.showinfo("提示", "请先加载FCS数据")
            return
            
        param1 = self.param1_var.get()
        param2 = self.param2_var.get()
        
        if not param1 or not param2:
            tk.messagebox.showwarning("警告", "请选择要绘制的参数")
            return
            
        # 清除旧图
        self.fig.clear()
        
        # 绘制散点图
        ax = self.fig.add_subplot(111)
        ax.scatter(self.raw_data[param1], self.raw_data[param2], s=1, alpha=0.5)
        ax.set_xlabel(param1)
        ax.set_ylabel(param2)
        ax.set_title(f"{param1} vs {param2}")
        
        # 添加门控范围
        try:
            min_val = float(self.min_var.get())
            max_val = float(self.max_var.get())
            ax.axhspan(min_val, max_val, alpha=0.2, color='red')
        except ValueError:
            pass
            
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _apply_gate(self):
        """应用门控按钮回调"""
        if self.raw_data is None:
            tk.messagebox.showinfo("提示", "请先加载FCS数据")
            return
            
        param1 = self.param1_var.get()
        param2 = self.param2_var.get()
        
        if not param1 or not param2:
            tk.messagebox.showwarning("警告", "请选择要门控的参数")
            return
            
        try:
            min_val = float(self.min_var.get())
            max_val = float(self.max_var.get())
        except ValueError:
            tk.messagebox.showerror("错误", "门控范围必须是数字")
            return
            
        # 执行门控
        gated_data, desc = self._gate_data(param1, param2, min_val, max_val)
        
        # 显示结果
        tk.messagebox.showinfo("门控结果", desc)
        
        # 更新图表
        self._plot_data()
    
    def _gate_data(self, param1, param2, min_val, max_val):
        """执行门控操作
        
        Args:
            param1: 参数1名称
            param2: 参数2名称
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            tuple: (门控后的数据, 处理描述)
        """
        # 根据param2的值筛选细胞
        mask = (self.raw_data[param2] >= min_val) & (self.raw_data[param2] <= max_val)
        gated_data = self.raw_data[mask]
        
        # 生成描述
        total_cells = len(self.raw_data)
        gated_cells = len(gated_data)
        percentage = (gated_cells / total_cells) * 100 if total_cells > 0 else 0
        
        desc = f"门控结果: 在{param2}参数范围[{min_val}, {max_val}]内筛选出{gated_cells}个细胞，占总数的{percentage:.2f}%"
        
        return gated_data, desc 