# GIF Maker

将多张图片合并成一张GIF动态图片的跨平台工具。

## 功能特点

- 将多张图片合并成一张GIF动态图片
- 支持设置帧延迟时间
- 支持多种图片格式
- 跨平台支持：Windows、macOS Intel、macOS ARM架构和Linux

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

### Linux

下载`linux`目录中的`gif-maker`文件，通过终端使用：

```bash
chmod +x gif-maker
./gif-maker -i 图片目录 -o 输出文件名.gif
```

## 从源代码构建

如果您想从源代码构建可执行文件，请按照以下步骤操作：

1. 安装Python 3.13或更高版本
2. 创建并激活虚拟环境：

```bash
# 创建名为git_env的虚拟环境
python3 -m venv git_env

# 在Windows上激活虚拟环境
# git_env\Scripts\activate

# 在macOS/Linux上激活虚拟环境
source git_env/bin/activate
```

3. 安装依赖：`pip install -r requirements.txt`
4. 运行构建脚本：`python build.py`
5. 完成后可以退出虚拟环境：`deactivate`

构建完成后，可执行文件将位于`dist`目录中。

使用虚拟环境可以确保项目依赖不会与系统Python环境冲突，并且便于管理项目特定的依赖包。

## 使用GitHub Actions自动发布

本项目配置了GitHub Actions工作流，可以自动构建并发布跨平台的可执行文件。

### 发布新版本

1. 确保所有代码变更已提交到仓库
2. 使用提供的发布脚本创建新版本：

```bash
# 发布版本1.0.0
./release.sh 1.0.0
```

3. 脚本会创建标签并推送到GitHub，触发GitHub Actions工作流
4. GitHub Actions将自动构建四种平台版本的可执行文件：
   - Windows
   - macOS Intel (x86_64)
   - macOS Apple Silicon (ARM64)
   - Linux
5. 构建完成后，可执行文件将自动上传到GitHub Releases页面

### 工作流说明

- 工作流配置文件位于`.github/workflows/build-and-release.yml`
- 工作流在推送以`v`开头的标签时触发（例如`v1.0.0`）
- 工作流会并行构建四种平台版本的可执行文件，包括两种macOS架构（Intel和Apple Silicon）
- 构建完成后，工作流会创建一个新的GitHub Release并上传所有可执行文件
