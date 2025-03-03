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
    """Check if target file exists"""
    print("Checking target file...")
    if TARGET_FILE.exists():
        print(f"Using existing {TARGET_FILE} file")
    else:
        print(f"Error: Target file {TARGET_FILE} does not exist")
        sys.exit(1)

def install_dependencies():
    """Install dependencies"""
    print("Installing dependencies...")
    
    try:
        # Install dependencies using requirements.txt
        requirements_file = Path(ROOT_DIR, "requirements.txt")
        if requirements_file.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
            print("Dependencies installed successfully")
        else:
            print(f"Warning: requirements.txt file does not exist, will install default dependencies")
            dependencies = ["pyinstaller", "pillow"]
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade"] + dependencies, check=True)
            print("Default dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def build_executable(target_platform=None, target_arch=None):
    """Build executable file
    
    Args:
        target_platform: Target platform, can be 'windows', 'macos', 'linux' or None (current platform)
        target_arch: Target architecture, can be 'x86_64', 'arm64' or None (current architecture)
    """
    current_platform = platform.system().lower()
    current_arch = platform.machine().lower()
    
    # If target platform is not specified, use current platform
    if target_platform is None:
        target_platform = current_platform
    
    # If target architecture is not specified, use current architecture
    if target_arch is None:
        target_arch = current_arch
    
    print(f"Building executable for {target_platform} ({target_arch})...")
    
    # Ensure output directory exists
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # Build command
    cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--clean",
        "--onefile",
        "--name", f"gif-maker-{target_platform}-{target_arch}",
        str(TARGET_FILE)
    ]
    
    # Add platform-specific options
    if target_platform == "windows" and current_platform != "windows":
        print("Warning: Building Windows executable on non-Windows platform may require Wine")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully built executable for {target_platform} ({target_arch})")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        if target_platform != current_platform or target_arch != current_arch:
            print(f"Skipping {target_platform} ({target_arch}) platform build")
            return False
        else:
            sys.exit(1)

def create_distribution_package():
    """Create distribution package"""
    print("Creating distribution package...")
    
    # Create distribution directory structure
    dist_macos_x64 = Path(DIST_DIR, "macos", "x64")
    dist_macos_arm64 = Path(DIST_DIR, "macos", "arm64")
    dist_windows = Path(DIST_DIR, "windows")
    dist_linux = Path(DIST_DIR, "linux")
    
    os.makedirs(dist_macos_x64, exist_ok=True)
    os.makedirs(dist_macos_arm64, exist_ok=True)
    os.makedirs(dist_windows, exist_ok=True)
    os.makedirs(dist_linux, exist_ok=True)
    
    # Get current system information
    current_system = platform.system().lower()
    current_machine = platform.machine().lower()
    
    # Define platforms and architectures to build
    platforms = [
        ("windows", "x86_64"),
        ("macos", "x86_64"),
        ("macos", "arm64"),
        ("linux", "x86_64")
    ]
    
    # Build executable for each platform
    for target_platform, target_arch in platforms:
        # Skip if not current platform and architecture
        if (target_platform != current_system or target_arch != current_machine) and not (current_system == "darwin" and target_platform == "macos"):
            print(f"Note: Skipping {target_platform} ({target_arch}) platform build because current system does not match")
            continue
            
        # Build executable
        success = build_executable(target_platform, target_arch)
        if not success:
            continue
        
        # Determine source file name and target directory
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
        
        # Copy file to target directory
        source_path = Path(ROOT_DIR, "dist", source_name)
        target_path = Path(target_dir, target_name)
        
        if source_path.exists():
            shutil.copy2(source_path, target_path)
            print(f"Copied {target_platform} {target_arch} executable to {target_dir}")
            
            # Set executable permissions for Linux and macOS
            if target_platform in ["linux", "macos"] and current_system in ["linux", "darwin"]:
                os.chmod(target_path, 0o755)
                print(f"Set executable permissions for {target_path}")
    
    print("Distribution package creation complete")

def create_readme():
    """Create README file"""
    # We no longer create README file because it already exists and has been modified by the user
    readme_path = Path(ROOT_DIR, "README.md")
    if readme_path.exists():
        print(f"Using existing README file: {readme_path}")
    else:
        print(f"Warning: README file does not exist: {readme_path}")

def clean_up():
    """Clean up temporary files"""
    print("Cleaning up temporary files...")
    
    # Clean up PyInstaller generated temporary files
    for spec_file in ROOT_DIR.glob("*.spec"):
        os.remove(spec_file)
        print(f"Deleted spec file: {spec_file}")
    
    # Clean up build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"Deleted build directory: {BUILD_DIR}")
    
    print("Temporary files cleanup complete")

def main():
    # 使用ASCII字符，避免Windows编码问题
    print("Starting to package GIF Maker...")
    
    # 执行打包步骤
    check_target_file()
    install_dependencies()
    build_executable()
    create_distribution_package()
    create_readme()
    clean_up()
    
    print("Packaging complete! Distribution packages are in the dist directory.")
    print("Supported platforms:")
    print("- macOS Intel (x64): dist/macos/x64")
    print("- macOS ARM (arm64): dist/macos/arm64")
    print("- Windows: dist/windows")
    print("- Linux: dist/linux")

if __name__ == "__main__":
    main()
