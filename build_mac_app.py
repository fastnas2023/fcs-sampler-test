import PyInstaller.__main__
import sys
import os
import shutil

def build_mac_app():
    # 确保我们在macOS上
    if sys.platform != 'darwin':
        print("此脚本只能在macOS上运行")
        return
    
    # 基本配置
    app_name = 'FCS细胞采样工具'
    main_script = 'fcs_sampler_gui.py'
    icon_file = 'app_icon.icns'
    
    # 清理旧的构建文件
    if os.path.exists('dist'):
        try:
            shutil.rmtree('dist')
            print("已清理旧的dist目录")
        except:
            print("无法清理dist目录，请手动删除")
    
    if os.path.exists('build'):
        try:
            shutil.rmtree('build')
            print("已清理旧的build目录")
        except:
            print("无法清理build目录，请手动删除")
    
    # PyInstaller参数
    params = [
        main_script,
        '--name=%s' % app_name,
        '--onefile',  # 生成单个可执行文件
        '--windowed',  # 使用GUI模式，不显示控制台
        '--clean',
        '--noconfirm',
        '--add-data=%s:%s' % ('app_icon.ico', '.'),
        '--add-data=%s:%s' % ('app_icon.icns', '.'),
        '--add-data=%s:%s' % ('app_icon.png', '.'),
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
        '--hidden-import=matplotlib',
        '--hidden-import=scipy',
    ])
    
    # 运行PyInstaller
    PyInstaller.__main__.run(params)
    
    # 设置权限
    app_path = os.path.join('dist', f'{app_name}.app')
    if os.path.exists(app_path):
        os.system(f'chmod -R 755 "{app_path}"')
        print(f"已设置{app_path}的权限")
        
        # 移除隔离属性
        os.system(f'xattr -rd com.apple.quarantine "{app_path}"')
        print(f"已移除{app_path}的隔离属性")
        
        print(f"应用程序已构建完成: {app_path}")
        print("如果应用程序仍然无法启动，请尝试在终端中运行:")
        print(f"open {app_path}")
    else:
        print("应用程序构建失败")

if __name__ == "__main__":
    build_mac_app() 