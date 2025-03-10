import tkinter as tk
from tkinter import ttk
import webbrowser

def open_website(url):
    webbrowser.open_new(url)

root = tk.Tk()
root.title("官网链接示例")
root.geometry("400x200")

frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

# 添加工作室名称和官网链接
studio_label = ttk.Label(frame, text="由 ", font=('Arial', 12))
studio_label.pack(side=tk.LEFT)

# 创建可点击的链接标签
website_label = ttk.Label(frame, text="cn111.net", foreground="blue", cursor="hand2", font=('Arial', 12, 'underline'))
website_label.pack(side=tk.LEFT)
website_label.bind("<Button-1>", lambda e: open_website("http://cn111.net"))

studio_label2 = ttk.Label(frame, text=" 工作室开发", font=('Arial', 12))
studio_label2.pack(side=tk.LEFT)

root.mainloop()