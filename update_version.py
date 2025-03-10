#!/usr/bin/env python3
"""
版本更新脚本
用法：
  python update_version.py [major|minor|patch]
  
例如：
  python update_version.py patch  # 增加补丁版本号 (1.0.0 -> 1.0.1)
  python update_version.py minor  # 增加次要版本号 (1.0.0 -> 1.1.0)
  python update_version.py major  # 增加主要版本号 (1.0.0 -> 2.0.0)
"""

import sys
import os

def read_version():
    """读取当前版本号"""
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    return version

def write_version(version):
    """写入新版本号"""
    with open('version.txt', 'w') as f:
        f.write(version)
    print(f"版本已更新为: {version}")

def update_version(version_type):
    """更新版本号"""
    current_version = read_version()
    major, minor, patch = map(int, current_version.split('.'))
    
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    else:
        print(f"错误: 未知的版本类型 '{version_type}'")
        print("用法: python update_version.py [major|minor|patch]")
        sys.exit(1)
    
    new_version = f"{major}.{minor}.{patch}"
    write_version(new_version)
    return new_version

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python update_version.py [major|minor|patch]")
        sys.exit(1)
    
    version_type = sys.argv[1].lower()
    update_version(version_type) 