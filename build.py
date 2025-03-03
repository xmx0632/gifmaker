#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GIF Maker打包脚本
用于将gif_maker.py打包成跨平台的可执行文件
支持Windows、macOS Intel和macOS ARM架构、Linux
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
    
    try:
        # 使用requirements.txt安装依赖
        requirements_file = Path(ROOT_DIR, "requirements.txt")
        if requirements_file.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
            print("依赖包安装成功")
        else:
            print(f"警告: requirements.txt文件不存在，将安装默认依赖")
            dependencies = ["pyinstaller", "pillow"]
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade"] + dependencies, check=True)
            print("默认依赖包安装成功")
    except subprocess.CalledProcessError as e:
        print(f"安装依赖包时出错: {e}")
        sys.exit(1)

def build_executable(target_platform=None, target_arch=None):
    """构建可执行文件
    
    参数:
        target_platform: 目标平台，可以是 'windows', 'macos', 'linux' 或 None (当前平台)
        target_arch: 目标架构，可以是 'x86_64', 'arm64' 或 None (当前架构)
    """
    current_platform = platform.system().lower()
    current_arch = platform.machine().lower()
    
    # 如果没有指定目标平台，则使用当前平台
    if target_platform is None:
        target_platform = current_platform
    
    # 如果没有指定目标架构，则使用当前架构
    if target_arch is None:
        target_arch = current_arch
    
    print(f"开始为 {target_platform} ({target_arch}) 构建可执行文件...")
    
    # 确保输出目录存在
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # 构建命令
    cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--clean",
        "--onefile",
        "--name", f"gif-maker-{target_platform}-{target_arch}",
        str(TARGET_FILE)
    ]
    
    # 添加平台特定选项
    if target_platform == "windows" and current_platform != "windows":
        print("警告: 在非Windows平台上构建Windows可执行文件可能需要Wine")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"为 {target_platform} ({target_arch}) 构建可执行文件成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建可执行文件时出错: {e}")
        if target_platform != current_platform or target_arch != current_arch:
            print(f"跳过 {target_platform} ({target_arch}) 平台构建")
            return False
        else:
            sys.exit(1)

def create_distribution_package():
    """创建分发包"""
    print("创建分发包...")
    
    # 创建分发目录结构
    dist_macos_x64 = Path(DIST_DIR, "macos", "x64")
    dist_macos_arm64 = Path(DIST_DIR, "macos", "arm64")
    dist_windows = Path(DIST_DIR, "windows")
    dist_linux = Path(DIST_DIR, "linux")
    
    os.makedirs(dist_macos_x64, exist_ok=True)
    os.makedirs(dist_macos_arm64, exist_ok=True)
    os.makedirs(dist_windows, exist_ok=True)
    os.makedirs(dist_linux, exist_ok=True)
    
    # 获取当前系统信息
    current_system = platform.system().lower()
    current_machine = platform.machine().lower()
    
    # 定义要构建的平台和架构
    platforms = [
        ("windows", "x86_64"),
        ("macos", "x86_64"),
        ("macos", "arm64"),
        ("linux", "x86_64")
    ]
    
    # 为每个平台构建可执行文件
    for target_platform, target_arch in platforms:
        # 如果不是当前平台和架构，跳过
        if (target_platform != current_system or target_arch != current_machine) and not (current_system == "darwin" and target_platform == "macos"):
            print(f"注意: 跳过 {target_platform} ({target_arch}) 平台构建，因为当前系统不匹配")
            continue
            
        # 构建可执行文件
        success = build_executable(target_platform, target_arch)
        if not success:
            continue
        
        # 确定源文件名和目标目录
        source_name = f"gif-maker-{target_platform}-{target_arch}"
        if target_platform == "windows":
            source_name += ".exe"
            target_dir = dist_windows
            target_name = "gif-maker.exe"
        elif target_platform == "macos":
            if target_arch == "arm64":
                target_dir = dist_macos_arm64
            else:
                target_dir = dist_macos_x64
            target_name = "gif-maker"
        elif target_platform == "linux":
            target_dir = dist_linux
            target_name = "gif-maker"
        
        # 复制文件到目标目录
        source_path = Path(ROOT_DIR, "dist", source_name)
        target_path = Path(target_dir, target_name)
        
        if source_path.exists():
            shutil.copy2(source_path, target_path)
            print(f"已复制 {target_platform} {target_arch} 可执行文件到 {target_dir}")
            
            # 为Linux和macOS设置可执行权限
            if target_platform in ["linux", "macos"] and current_system in ["linux", "darwin"]:
                os.chmod(target_path, 0o755)
                print(f"已设置 {target_path} 的可执行权限")
    
    print("分发包创建完成")

def create_readme():
    """创建README文件"""
    # 我们不再创建README文件，因为它已经存在并被用户修改过
    readme_path = Path(ROOT_DIR, "README.md")
    if readme_path.exists():
        print(f"使用现有README文件: {readme_path}")
    else:
        print(f"警告: README文件不存在: {readme_path}")

def clean_up():
    """清理临时文件"""
    print("清理临时文件...")
    
    # 清理PyInstaller生成的临时文件
    for spec_file in ROOT_DIR.glob("*.spec"):
        os.remove(spec_file)
        print(f"已删除规格文件: {spec_file}")
    
    # 清理构建目录
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"已删除构建目录: {BUILD_DIR}")
    
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
    print("- Linux: dist/linux")

if __name__ == "__main__":
    main()
