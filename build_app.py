import PyInstaller.__main__
import sys
import os
import subprocess

def build_app():
    # 确定当前操作系统
    is_mac = sys.platform == 'darwin'
    is_windows = sys.platform == 'win32'
    
    # 基本配置
    app_name = 'FCS细胞采样工具'
    main_script = 'fcs_sampler_gui.py'
    icon_file = 'app_icon.icns' if is_mac else 'app_icon.ico'
    
    # PyInstaller参数
    params = [
        main_script,
        '--name=%s' % app_name,
        '--onefile',  # 生成单个可执行文件
        '--noconsole' if is_windows else '--windowed',  # Windows使用noconsole
        '--clean',
        '--noconfirm',
        '--add-data=%s%s%s' % (
            'app_icon.ico',
            ';' if is_windows else ':',
            '.'
        ),
    ]
    
    # 添加图标
    if os.path.exists(icon_file):
        params.append('--icon=%s' % icon_file)
    
    # 添加所需包
    params.extend([
        '--hidden-import=numpy',
        '--hidden-import=pandas',
        '--hidden-import=fcsparser',
        '--hidden-import=flowio',
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--hidden-import=matplotlib',  # 添加matplotlib
        '--hidden-import=scipy',       # 添加scipy
    ])
    
    # Mac特定配置
    if is_mac:
        params.extend([
            '--osx-bundle-identifier=com.fcs.sampler',  # 添加bundle identifier
        ])
    
    # Windows特定配置
    if is_windows:
        params.extend([
            '--runtime-hook=windows_hook.py',  # 添加Windows运行时钩子
        ])
    
    # 运行PyInstaller
    PyInstaller.__main__.run(params)
    
    # Mac特定后处理
    if is_mac:
        # 设置应用程序权限
        app_path = os.path.join('dist', f'{app_name}.app')
        if os.path.exists(app_path):
            # 修复权限
            subprocess.run(['chmod', '-R', '+x', app_path])
            # 移除隔离属性
            subprocess.run(['xattr', '-rd', 'com.apple.quarantine', app_path])

if __name__ == "__main__":
    build_app() 