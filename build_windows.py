import os
import subprocess

def build_windows_exe():
    # Wine Python 路径
    wine_python = 'wine python'
    
    # 安装必要的包
    packages = [
        'pyinstaller',
        'numpy',
        'pandas',
        'fcsparser',
        'flowio',
        'pillow'
    ]
    
    for package in packages:
        os.system(f'{wine_python} -m pip install {package}')
    
    # 运行 PyInstaller
    build_command = f'{wine_python} -m PyInstaller FCS细胞采样工具_windows.spec'
    os.system(build_command)

if __name__ == '__main__':
    build_windows_exe() 