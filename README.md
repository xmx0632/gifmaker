# GIF Maker

A cross-platform tool for combining multiple images or video clips into a single animated GIF.

## Features

- Combine multiple images into an animated GIF
- **Extract frames from video files to create GIFs**
- Customize frame delay time
- Support for various image formats
- **Resize images of different sizes to a uniform dimension**
- Cross-platform support: Windows, macOS (Intel & ARM architecture), and Linux

## Usage

### Command Line Usage

#### Creating GIFs from Images

```bash
# Basic usage
./gif-maker images -i image_directory -o output_filename.gif -d frame_delay_ms

# Example
./gif-maker images -i ./images -o output.gif -d 200

# Using different file matching pattern
./gif-maker images -i ./images -o output.gif -d 200 -p "*.jpg"

# Creating GIF with resized images
./gif-maker images -i ./images -o resized.gif -d 200 -r -w 800 --height 600

# Legacy syntax (not recommended)
./gif-maker -i ./images -o output.gif -d 100
```

#### Creating GIFs from Videos

```bash
# Basic usage - extract the entire video
./gif-maker video -i input.mp4 -o output.gif

# Extract a specific segment (5 to 10 seconds)
./gif-maker video -i input.mp4 -o clip.gif -s 5 -e 10

# Adjust frame rate and size
./gif-maker video -i input.mp4 -o resized.gif -f 15 -r -w 640 --height 480
```

### Parameter Description

#### Common Parameters
- `-o, --output`: Output GIF file path (required)
- `-r, --resize`: Whether to resize images
- `-w, --width`: Width of resized images
- `--height`: Height of resized images
- `-k, --keep-aspect-ratio`: Whether to maintain the original aspect ratio (default: yes)
- `--fill-mode`: Fill mode when maintaining aspect ratio:
  - `fill`: Scale and crop to fill the entire frame (default)
  - `center`: Center the image, possibly leaving transparent areas

#### Image Mode Parameters
- `-i, --input`: Input image directory (required)
- `-d, --duration`: Delay time for each frame in milliseconds, default is 100
- `-p, --pattern`: File matching pattern, default is "*.png"

#### Video Mode Parameters
- `-i, --input`: Input video file path (required)
- `-s, --start`: Start time in seconds, default is 0
- `-e, --end`: End time in seconds, default is the end of the video
- `-f, --fps`: Frames to extract per second, default is 10
- `-d, --duration`: Delay time for each frame in milliseconds, default is automatically calculated based on fps

## Installation

This tool provides pre-compiled executables that can be used without installing Python or other dependencies.

> **Note**: Video processing functionality requires the OpenCV library. If you're using the pre-compiled version, this dependency is already included. If running from source code, you'll need to install the `opencv-python` package separately.

### Windows

Download the `gif-maker.exe` file from the `windows` directory, then double-click to run or use it via command line.

### macOS Intel (x64)

Download the `gif-maker` file from the `macos/x64` directory, then use it via terminal:

```bash
chmod +x gif-maker
./gif-maker -i image_directory -o output_filename.gif
```

### macOS ARM (Apple Silicon)

Download the `gif-maker` file from the `macos/arm64` directory, then use it via terminal:

```bash
chmod +x gif-maker
./gif-maker -i image_directory -o output_filename.gif
```

### Linux

Download the `gif-maker` file from the `linux` directory, then use it via terminal:

```bash
chmod +x gif-maker
./gif-maker -i image_directory -o output_filename.gif
```

## Building from Source

If you want to build the executable from source code, follow these steps:

1. Install Python 3.13 or higher
2. Create and activate a virtual environment:

```bash
# Create a virtual environment named git_env
python3 -m venv git_env

# Activate the virtual environment on Windows
# git_env\Scripts\activate

# Activate the virtual environment on macOS/Linux
source git_env/bin/activate
```

3. Install dependencies:
   ```bash
   # Basic functionality
   pip install Pillow
   
   # Video processing functionality (optional)
   pip install opencv-python
   
   # Or install all dependencies at once
   pip install -r requirements.txt
   ```

4. Run the build script: `python build.py`
5. When finished, you can deactivate the virtual environment: `deactivate`

After building, the executable will be located in the `dist` directory.

Using a virtual environment ensures that project dependencies don't conflict with your system Python environment and makes it easier to manage project-specific packages.

## Automated Releases with GitHub Actions

This project is configured with GitHub Actions workflows to automatically build and release cross-platform executables.

### Releasing a New Version

#### Method 1: Using the Release Script

1. Ensure all code changes are committed to the repository
2. Use the provided release script to create a new version:

```bash
# Release version 1.0.0
./release.sh 1.0.0
```

3. The script will create a tag and push it to GitHub, triggering the GitHub Actions workflow

#### Method 2: Manual Trigger via GitHub Web Interface

1. On the GitHub repository page, click the "Actions" tab
2. Select "Build and Release" from the workflow list on the left
3. Click the "Run workflow" button
4. Enter the version number (e.g., 1.0.0) and select whether it's a pre-release
5. Click "Run workflow" to start the build

#### Build Results

GitHub Actions will automatically build executables for four platforms:
- Windows
- macOS Intel (x86_64)
- macOS Apple Silicon (ARM64)
- Linux

After the build is complete, the executables will be automatically uploaded to the GitHub Releases page.

### Workflow Details

- The workflow configuration is located in `.github/workflows/build-and-release.yml`
- The workflow can be triggered in two ways:
  - Automatically when a tag starting with `v` is pushed (e.g., `v1.0.0`)
  - Manually from the GitHub Actions page, specifying a version number
- The workflow builds executables for four platforms in parallel, including two macOS architectures (Intel and Apple Silicon)
- The workflow uses dependency caching to significantly reduce installation time and improve build speed
- Caching is based on the hash of the `requirements.txt` file, only reinstalling when dependencies change
- After building, the workflow creates a new GitHub Release and uploads all executables

## Donation

If you find this tool useful, consider supporting its development:

| **Alipay** | **WeChat Pay** |
| :---: | :---: |
| <img src="doc/donate/alipay-2.png" width="250px"> | <img src="doc/donate/wechat-pay.jpg" width="250px"> |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
