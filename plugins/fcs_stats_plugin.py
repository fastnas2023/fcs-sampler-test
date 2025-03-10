"""
FCS统计分析插件 - 用于对FCS数据进行统计分析
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 导入插件接口
from fcs_sampler_gui import FcsPluginInterface

class FcsStatsPlugin(FcsPluginInterface):
    """FCS统计分析插件，用于对FCS数据进行统计分析"""
    
    def __init__(self):
        super().__init__()
        self.name = "FCS统计分析插件"
        self.description = "对FCS数据进行统计分析，包括直方图、基本统计量等"
        self.version = "1.0.0"
        self.author = "FCS工具开发团队"
        
        # 插件UI元素
        self.ui_frame = None
        self.param_var = None
        self.bins_var = None
        self.canvas = None
        self.fig = None
        self.stats_text = None
        
        # 数据
        self.metadata = None
        self.raw_data = None
        self.param_names = []
    
    def get_ui_elements(self, parent_frame):
        """创建插件UI元素"""
        self.ui_frame = ttk.Frame(parent_frame)
        
        # 参数选择部分
        param_frame = ttk.LabelFrame(self.ui_frame, text="分析参数", padding=10)
        param_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 参数选择
        ttk.Label(param_frame, text="选择参数:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.param_var = tk.StringVar()
        self.param_combo = ttk.Combobox(param_frame, textvariable=self.param_var, state="readonly")
        self.param_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # 直方图设置
        ttk.Label(param_frame, text="直方图分箱数:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.bins_var = tk.StringVar(value="50")
        ttk.Entry(param_frame, textvariable=self.bins_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=(10, 0))
        
        # 操作按钮
        button_frame = ttk.Frame(self.ui_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="加载数据", command=self._load_data)
        load_button.pack(side=tk.LEFT, padx=5)
        
        hist_button = ttk.Button(button_frame, text="绘制直方图", command=self._plot_histogram)
        hist_button.pack(side=tk.LEFT, padx=5)
        
        stats_button = ttk.Button(button_frame, text="计算统计量", command=self._calculate_stats)
        stats_button.pack(side=tk.LEFT, padx=5)
        
        export_button = ttk.Button(button_frame, text="导出统计结果", command=self._export_stats)
        export_button.pack(side=tk.LEFT, padx=5)
        
        # 创建分割窗格
        paned = ttk.PanedWindow(self.ui_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 图表区域
        plot_frame = ttk.LabelFrame(paned, text="数据可视化", padding=10)
        paned.add(plot_frame, weight=2)
        
        # 创建matplotlib图形
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 初始状态提示
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, "请先加载FCS数据", ha='center', va='center', fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
        
        # 统计结果区域
        stats_frame = ttk.LabelFrame(paned, text="统计结果", padding=10)
        paned.add(stats_frame, weight=1)
        
        # 创建文本框显示统计结果
        self.stats_text = tk.Text(stats_frame, wrap=tk.WORD, height=8)
        self.stats_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.stats_text['yscrollcommand'] = scrollbar.set
        
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
        if self.param_combo:
            self.param_combo["values"] = self.param_names
            if len(self.param_names) > 0:
                self.param_combo.current(0)
        
        # 如果提供了参数，执行统计分析
        if params and 'param' in params:
            return self._analyze_data(params['param'])
        
        return raw_data, "数据已加载，未进行统计分析"
    
    def _load_data(self):
        """加载数据按钮回调"""
        if self.raw_data is None:
            messagebox.showinfo("提示", "请先在主界面加载FCS文件，然后点击'加载插件'按钮")
            return
            
        # 更新UI
        messagebox.showinfo("成功", f"已加载FCS数据，共{len(self.raw_data)}个细胞，{len(self.param_names)}个参数")
    
    def _plot_histogram(self):
        """绘制直方图按钮回调"""
        if self.raw_data is None:
            messagebox.showinfo("提示", "请先加载FCS数据")
            return
            
        param = self.param_var.get()
        
        if not param:
            messagebox.showwarning("警告", "请选择要分析的参数")
            return
            
        try:
            bins = int(self.bins_var.get())
            if bins <= 0:
                raise ValueError("分箱数必须大于0")
        except ValueError as e:
            messagebox.showerror("错误", f"分箱数设置错误: {str(e)}")
            return
            
        # 清除旧图
        self.fig.clear()
        
        # 绘制直方图
        ax = self.fig.add_subplot(111)
        ax.hist(self.raw_data[param], bins=bins, alpha=0.7)
        ax.set_xlabel(param)
        ax.set_ylabel("频数")
        ax.set_title(f"{param}的分布直方图")
            
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _calculate_stats(self):
        """计算统计量按钮回调"""
        if self.raw_data is None:
            messagebox.showinfo("提示", "请先加载FCS数据")
            return
            
        param = self.param_var.get()
        
        if not param:
            messagebox.showwarning("警告", "请选择要分析的参数")
            return
            
        # 计算统计量
        data = self.raw_data[param]
        stats = {
            "参数": param,
            "样本数": len(data),
            "最小值": np.min(data),
            "最大值": np.max(data),
            "平均值": np.mean(data),
            "中位数": np.median(data),
            "标准差": np.std(data),
            "变异系数": (np.std(data) / np.mean(data)) * 100 if np.mean(data) != 0 else 0,
            "偏度": float(pd.Series(data).skew()),
            "峰度": float(pd.Series(data).kurtosis())
        }
        
        # 显示统计结果
        self.stats_text.delete(1.0, tk.END)
        for key, value in stats.items():
            if isinstance(value, (int, np.integer)):
                self.stats_text.insert(tk.END, f"{key}: {value}\n")
            else:
                self.stats_text.insert(tk.END, f"{key}: {value:.4f}\n")
    
    def _export_stats(self):
        """导出统计结果按钮回调"""
        if self.raw_data is None or not self.stats_text.get(1.0, tk.END).strip():
            messagebox.showinfo("提示", "请先计算统计量")
            return
            
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                title="保存统计结果"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"FCS文件统计分析结果\n")
                    f.write(f"分析时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(self.stats_text.get(1.0, tk.END))
                
                messagebox.showinfo("成功", f"统计结果已保存到: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出统计结果时出错: {str(e)}")
    
    def _analyze_data(self, param):
        """分析数据
        
        Args:
            param: 要分析的参数名称
            
        Returns:
            tuple: (原始数据, 分析描述)
        """
        if param not in self.raw_data.columns:
            return self.raw_data, f"参数 {param} 不存在"
            
        # 计算基本统计量
        data = self.raw_data[param]
        mean = np.mean(data)
        median = np.median(data)
        std = np.std(data)
        
        desc = f"参数 {param} 的统计分析结果:\n"
        desc += f"样本数: {len(data)}\n"
        desc += f"平均值: {mean:.4f}\n"
        desc += f"中位数: {median:.4f}\n"
        desc += f"标准差: {std:.4f}\n"
        
        return self.raw_data, desc 