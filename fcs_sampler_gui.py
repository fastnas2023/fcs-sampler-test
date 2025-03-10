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

class FcsSamplerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FCS文件细胞采样工具")
        self.root.geometry("700x850")  # 调整窗口大小以适应新布局
        self.root.configure(bg="#f5f5f5")  # 设置背景颜色
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建标题和工作室信息框架
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 添加标题
        title_label = ttk.Label(header_frame, text="FCS文件细胞采样工具", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 添加工作室信息和官网链接
        studio_frame = ttk.Frame(header_frame)
        studio_frame.grid(row=0, column=1, sticky=tk.E)
        
        studio_label = ttk.Label(studio_frame, text="由 ", font=('Arial', 10))
        studio_label.pack(side=tk.LEFT)
        
        # 创建可点击的链接标签
        website_label = ttk.Label(studio_frame, text="cn111.net", foreground="blue", cursor="hand2", font=('Arial', 10, 'underline'))
        website_label.pack(side=tk.LEFT)
        website_label.bind("<Button-1>", lambda e: self.open_website("http://cn111.net"))
        
        studio_label2 = ttk.Label(studio_frame, text=" 工作室开发", font=('Arial', 10))
        studio_label2.pack(side=tk.LEFT)
        
        # 设置列权重，使标题和工作室信息分别靠左和靠右
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        
        # 创建内容区域的选项卡
        tab_control = ttk.Notebook(main_frame)
        tab_control.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 创建"采样"选项卡
        sampling_tab = ttk.Frame(tab_control, padding=10)
        tab_control.add(sampling_tab, text="采样设置")
        
        # 创建"关于"选项卡
        about_tab = ttk.Frame(tab_control, padding=10)
        tab_control.add(about_tab, text="关于与支持")
        
        # ===== 采样选项卡内容 =====
        # 文件选择部分
        file_section = ttk.LabelFrame(sampling_tab, text="文件设置", padding=10)
        file_section.pack(fill=tk.X, pady=(0, 10))
        
        # 文件选择行
        file_frame = ttk.Frame(file_section)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="FCS文件:").grid(row=0, column=0, padx=5)
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="选择文件", command=self.select_file).grid(row=0, column=2, padx=5)
        
        # 输出目录行
        output_frame = ttk.Frame(file_section)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="输出目录:").grid(row=0, column=0, padx=5)
        self.output_dir = tk.StringVar(value=os.path.expanduser("~/Documents"))
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(output_frame, text="选择目录", command=self.select_output_dir).grid(row=0, column=2, padx=5)
        
        # 参数设置部分
        param_section = ttk.LabelFrame(sampling_tab, text="采样参数", padding=10)
        param_section.pack(fill=tk.X, pady=(0, 10))
        
        # 范围设置
        range_frame = ttk.Frame(param_section)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(range_frame, text="起始位置:").grid(row=0, column=0, padx=5)
        self.range_start = tk.StringVar(value="0")  # 改为0，表示第1个细胞
        ttk.Entry(range_frame, textvariable=self.range_start, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(range_frame, text="结束位置:").grid(row=0, column=2, padx=5)
        self.range_end = tk.StringVar(value="-1")  # 使用-1表示最后一个细胞
        ttk.Entry(range_frame, textvariable=self.range_end, width=15).grid(row=0, column=3, padx=5)
        
        # 采样设置
        sample_frame = ttk.Frame(param_section)
        sample_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(sample_frame, text="目标数量:").grid(row=0, column=0, padx=5)
        self.target_count = tk.StringVar(value="-1")  # 使用-1表示所有细胞
        ttk.Entry(sample_frame, textvariable=self.target_count, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(sample_frame, text="采样模式:").grid(row=0, column=2, padx=5)
        self.sample_mode = tk.StringVar(value="interval")
        mode_combo = ttk.Combobox(sample_frame, textvariable=self.sample_mode, width=15)
        mode_combo['values'] = ('continuous', 'interval', 'random')
        mode_combo.grid(row=0, column=3, padx=5)
        
        # 操作按钮
        button_frame = ttk.Frame(sampling_tab)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="开始采样", command=self.start_sampling, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除信息", command=self.clear_info).pack(side=tk.LEFT, padx=5)
        
        # 信息显示区域
        info_section = ttk.LabelFrame(sampling_tab, text="处理信息", padding=10)
        info_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.info_text = tk.Text(info_section, height=15, width=70)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.info_text, orient="vertical", command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        # ===== 关于选项卡内容 =====
        # 添加应用程序信息
        about_frame = ttk.Frame(about_tab, padding=10)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        # 应用程序描述
        desc_text = """FCS细胞采样工具是一个用于处理流式细胞仪数据的应用程序。
        
它可以帮助您从大型FCS文件中提取样本，支持多种采样模式：
• 连续采样：从指定位置开始连续提取指定数量的细胞
• 间隔采样：按固定间隔从指定范围内提取细胞
• 随机采样：从指定范围内随机提取指定数量的细胞

本工具由cn111.net工作室开发，版本1.0.2"""
        
        desc_label = ttk.Label(about_frame, text=desc_text, wraplength=600, justify=tk.LEFT)
        desc_label.pack(fill=tk.X, pady=(0, 20))
        
        # 打赏二维码部分
        donate_frame = ttk.LabelFrame(about_tab, text="打赏支持", padding=10)
        donate_frame.pack(fill=tk.X, pady=10)
        
        # 添加说明文字
        intro_text = "如果您觉得这个工具对您有所帮助，欢迎扫描下方二维码进行打赏支持！"
        ttk.Label(donate_frame, text=intro_text, wraplength=600).pack(pady=(0, 10))
        
        # 创建二维码容器框架
        qrcode_container = ttk.Frame(donate_frame)
        qrcode_container.pack(fill=tk.X)
        
        # 加载并显示微信二维码
        try:
            wechat_img = Image.open("qrcode-wechat.jpg")
            # 调整大小为更合适的尺寸
            wechat_img = wechat_img.resize((120, 120), Image.LANCZOS)
            self.wechat_photo = ImageTk.PhotoImage(wechat_img)
            
            # 创建微信支付框架
            wechat_frame = ttk.Frame(qrcode_container)
            wechat_frame.pack(side=tk.LEFT, padx=20, pady=5)
            
            # 添加微信二维码和标签
            wechat_label = ttk.Label(wechat_frame, image=self.wechat_photo)
            wechat_label.pack(pady=5)
            ttk.Label(wechat_frame, text="微信支付", font=('Arial', 10, 'bold')).pack()
        except Exception as e:
            print(f"加载微信二维码出错: {e}")
        
        # 加载并显示支付宝二维码
        try:
            alipay_img = Image.open("qrcode-alipay.jpg")
            # 调整大小为更合适的尺寸
            alipay_img = alipay_img.resize((120, 120), Image.LANCZOS)
            self.alipay_photo = ImageTk.PhotoImage(alipay_img)
            
            # 创建支付宝框架
            alipay_frame = ttk.Frame(qrcode_container)
            alipay_frame.pack(side=tk.LEFT, padx=20, pady=5)
            
            # 添加支付宝二维码和标签
            alipay_label = ttk.Label(alipay_frame, image=self.alipay_photo)
            alipay_label.pack(pady=5)
            ttk.Label(alipay_frame, text="支付宝", font=('Arial', 10, 'bold')).pack()
        except Exception as e:
            print(f"加载支付宝二维码出错: {e}")
            
        # 添加感谢文字
        thank_text = "感谢您的支持，这将帮助我们持续改进和维护这个工具！"
        ttk.Label(donate_frame, text=thank_text, wraplength=600, font=('Arial', 10, 'italic')).pack(pady=10)
        
        # 添加版权信息
        copyright_frame = ttk.Frame(main_frame)
        copyright_frame.grid(row=2, column=0, sticky=(tk.E), pady=(5, 0))
        
        copyright_text = "© 2025 FCS细胞采样工具 - 版本 1.0.2"
        ttk.Label(copyright_frame, text=copyright_text, font=('Arial', 8)).pack(side=tk.RIGHT)
        
        # 设置样式
        self.setup_styles()
        
    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        
        # 设置按钮样式
        style.configure("Accent.TButton", font=('Arial', 11, 'bold'))
        
        # 设置标签框架样式
        style.configure("TLabelframe", borderwidth=2)
        style.configure("TLabelframe.Label", font=('Arial', 11, 'bold'))
        
        # 设置选项卡样式
        style.configure("TNotebook", tabposition='n')
        style.configure("TNotebook.Tab", font=('Arial', 10), padding=[10, 2])
        
    def open_website(self, url):
        """打开网站链接"""
        webbrowser.open_new(url)
        
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="选择FCS文件",
            filetypes=[("FCS files", "*.fcs"), ("All files", "*.*")]
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
            title="选择输出目录",
            initialdir=self.output_dir.get()
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
            
            # 准备输出数据
            cell_data = sampled_cells.values.flatten()
            if not np.issubdtype(cell_data.dtype, np.floating):
                cell_data = cell_data.astype(np.float32)
            
            # 更新元数据
            output_metadata = metadata.copy()
            output_metadata['$TOT'] = len(sampled_cells)
            
            # 生成输出文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'sampled_{range_start}-{range_end}_mode{sample_mode}_{timestamp}.fcs'
            output_file = os.path.join(output_dir, output_filename)
            
            # 写入新文件
            self.show_info("\n正在保存文件...")
            with open(output_file, 'wb') as f:
                flow_data = flowio.create_fcs(
                    f,
                    event_data=cell_data,
                    channel_names=[metadata[f'$P{i}N'] for i in range(1, metadata['$PAR']+1)]
                )
            
            self.show_info(f"文件已保存: {output_file}")
            messagebox.showinfo("成功", f"采样完成！\n文件已保存到：\n{output_file}")
            
        except Exception as e:
            self.show_info(f"\n错误: {str(e)}")
            messagebox.showerror("错误", str(e))

def sample_cells(raw_data, range_start, range_end, target_count, mode='continuous'):
    """
    细胞采样函数
    mode: 采样模式 - 'continuous'（连续）, 'interval'（间隔）, 'random'（随机）
    """
    cells_in_range = raw_data.iloc[range_start:range_end]
    range_count = len(cells_in_range)
    
    if mode == 'continuous':
        # 连续采样：直接取前target_count个细胞
        sampled_cells = cells_in_range.iloc[:target_count]
        sample_desc = f"连续采样前{target_count}个细胞"
        
    elif mode == 'interval':
        # 间隔采样：计算所需间隔
        interval = range_count // target_count
        if interval < 1:
            interval = 1
        sampled_cells = cells_in_range.iloc[::interval]
        sample_desc = f"每{interval}个细胞采样1个"
        
    elif mode == 'random':
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