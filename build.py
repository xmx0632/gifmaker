#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GIF Maker打包脚本
用于将gif.py打包成跨平台的可执行文件
支持Windows、macOS Intel和macOS ARM架构
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.absolute()
# 目标文件路径
TARGET_FILE = Path(ROOT_DIR, "gif_maker.py")
# 输出目录
DIST_DIR = Path(ROOT_DIR, "dist")
# 构建目录
BUILD_DIR = Path(ROOT_DIR, "build")

def check_target_file():
    """检查目标文件是否存在"""
    print("检查目标文件...")
    if TARGET_FILE.exists():
        print(f"使用现有的 {TARGET_FILE} 文件")
    else:
        print(f"错误: 目标文件 {TARGET_FILE} 不存在")
        sys.exit(1)

def install_dependencies():
    """安装依赖包"""
    print("安装依赖包...")
    dependencies = ["pyinstaller", "pillow"]
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade"] + dependencies, check=True)
        print("依赖包安装成功")
    except subprocess.CalledProcessError as e:
        print(f"安装依赖包时出错: {e}")
        sys.exit(1)

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 确保输出目录存在
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # 构建命令
    cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--clean",
        "--onefile",
        "--name", "gif-maker",
        str(TARGET_FILE)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("可执行文件构建成功")
    except subprocess.CalledProcessError as e:
        print(f"构建可执行文件时出错: {e}")
        sys.exit(1)

def create_distribution_package():
    """创建分发包"""
    print("创建分发包...")
    
    # 创建分发目录结构
    dist_macos_x64 = Path(DIST_DIR, "macos", "x64")
    dist_macos_arm64 = Path(DIST_DIR, "macos", "arm64")
    dist_windows = Path(DIST_DIR, "windows")
    
    os.makedirs(dist_macos_x64, exist_ok=True)
    os.makedirs(dist_macos_arm64, exist_ok=True)
    os.makedirs(dist_windows, exist_ok=True)
    
    # 获取当前系统信息
    system = platform.system()
    machine = platform.machine()
    
    # 移动构建的可执行文件到对应的目录
    exe_path = Path(ROOT_DIR, "dist", "gif-maker")
    if system == "Darwin":  # macOS
        if machine == "arm64":
            shutil.copy2(exe_path, Path(dist_macos_arm64, "gif-maker"))
            print(f"已复制 macOS ARM64 可执行文件到 {dist_macos_arm64}")
        else:
            shutil.copy2(exe_path, Path(dist_macos_x64, "gif-maker"))
            print(f"已复制 macOS x64 可执行文件到 {dist_macos_x64}")
    elif system == "Windows":
        exe_path = Path(ROOT_DIR, "dist", "gif-maker.exe")
        shutil.copy2(exe_path, Path(dist_windows, "gif-maker.exe"))
        print(f"已复制 Windows 可执行文件到 {dist_windows}")
    
    print("分发包创建完成")

def create_readme():
    """创建README文件"""
    readme_path = Path(ROOT_DIR, "README.md")
    
    readme_content = """# GIF Maker

将多张图片合并成一张GIF动态图片的跨平台工具。

## 功能特点

- 将多张图片合并成一张GIF动态图片
- 支持设置帧延迟时间
- 支持多种图片格式
- 跨平台支持：Windows、macOS Intel和macOS ARM架构

## 使用方法

### 命令行使用

```bash
# 基本用法
./gif-maker -i 图片目录 -o 输出文件名.gif -d 帧延迟(毫秒)

# 示例
./gif-maker -i ./images -o output.gif -d 200

# 使用不同的文件匹配模式
./gif-maker -i ./images -o output.gif -d 200 -p "*.jpg"
```

### 参数说明

- `-i, --input`: 输入图片目录（必需）
- `-o, --output`: 输出GIF文件路径（必需）
- `-d, --duration`: 每一帧的延迟时间，单位为毫秒，默认为100
- `-p, --pattern`: 文件匹配模式，默认为"*.png"

## 安装说明

本工具提供了预编译的可执行文件，无需安装Python或其他依赖即可使用。

### Windows

下载`windows`目录中的`gif-maker.exe`文件，双击运行或通过命令行使用。

### macOS Intel (x64)

下载`macos/x64`目录中的`gif-maker`文件，通过终端使用：

```bash
chmod +x gif-maker
./gif-maker -i 图片目录 -o 输出文件名.gif
```

### macOS ARM (Apple Silicon)

下载`macos/arm64`目录中的`gif-maker`文件，通过终端使用：

```bash
chmod +x gif-maker
./gif-maker -i 图片目录 -o 输出文件名.gif
```

## 从源代码构建

如果您想从源代码构建可执行文件，请按照以下步骤操作：

1. 安装Python 3.6或更高版本
2. 安装依赖：`pip install pyinstaller pillow`
3. 运行构建脚本：`python build.py`

构建完成后，可执行文件将位于`dist`目录中。
"""
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"README文件已创建：{readme_path}")

def clean_up():
    """清理临时文件"""
    print("清理临时文件...")
    
    # 清理PyInstaller生成的临时文件
    spec_file = Path(ROOT_DIR, "gif-maker.spec")
    if spec_file.exists():
        os.remove(spec_file)
    
    # 清理构建目录
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    print("临时文件清理完成")

def main():
    print("开始打包GIF Maker...")
    
    # 执行打包步骤
    check_target_file()
    install_dependencies()
    build_executable()
    create_distribution_package()
    create_readme()
    clean_up()
    
    print("打包完成！分发包位于dist目录中。")
    print("支持的平台：")
    print("- macOS Intel (x64): dist/macos/x64")
    print("- macOS ARM (arm64): dist/macos/arm64")
    print("- Windows: dist/windows")

if __name__ == "__main__":
    main()
