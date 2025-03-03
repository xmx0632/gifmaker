#!/bin/bash
# GIF Maker 安装脚本

# 检测操作系统和架构
OS="$(uname -s)"
ARCH="$(uname -m)"

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 目标安装目录
INSTALL_DIR="/usr/local/bin"

echo -e "${GREEN}开始安装 GIF Maker...${NC}"

# 检查是否有root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}注意: 没有root权限，将使用sudo安装到 $INSTALL_DIR${NC}"
        USE_SUDO=true
    else
        USE_SUDO=false
    fi
}

# 安装可执行文件
install_executable() {
    local source_file=""
    
    # 根据操作系统和架构选择正确的可执行文件
    if [ "$OS" = "Darwin" ]; then
        if [ "$ARCH" = "arm64" ]; then
            echo "检测到 macOS ARM (Apple Silicon) 系统"
            source_file="$SCRIPT_DIR/dist/macos/arm64/gif-maker"
        else
            echo "检测到 macOS Intel 系统"
            source_file="$SCRIPT_DIR/dist/macos/x64/gif-maker"
        fi
    elif [ "$OS" = "Linux" ]; then
        echo "检测到 Linux 系统"
        source_file="$SCRIPT_DIR/dist/linux/gif-maker"
    elif [[ "$OS" == MINGW* ]] || [[ "$OS" == CYGWIN* ]]; then
        echo -e "${RED}Windows系统请直接使用 dist/windows/gif-maker.exe 文件${NC}"
        echo "安装已取消"
        exit 1
    else
        echo -e "${RED}不支持的操作系统: $OS${NC}"
        echo "安装已取消"
        exit 1
    fi
    
    # 检查源文件是否存在
    if [ ! -f "$source_file" ]; then
        echo -e "${RED}错误: 找不到可执行文件 $source_file${NC}"
        echo "请先运行 build.py 构建可执行文件"
        exit 1
    fi
    
    # 安装可执行文件
    echo "正在安装 GIF Maker 到 $INSTALL_DIR..."
    
    if [ "$USE_SUDO" = true ]; then
        sudo cp "$source_file" "$INSTALL_DIR/gif-maker"
        sudo chmod +x "$INSTALL_DIR/gif-maker"
    else
        cp "$source_file" "$INSTALL_DIR/gif-maker"
        chmod +x "$INSTALL_DIR/gif-maker"
    fi
    
    # 检查安装是否成功
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}GIF Maker 安装成功!${NC}"
        echo -e "您可以通过运行 ${YELLOW}gif-maker -i 图片目录 -o 输出文件.gif${NC} 来使用它"
    else
        echo -e "${RED}安装失败!${NC}"
        exit 1
    fi
}

# 主函数
main() {
    check_root
    install_executable
}

# 执行主函数
main
