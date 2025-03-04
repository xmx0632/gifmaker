#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
将多张图片合并成一张GIF动态图片

使用方法：
1. 命令行运行: python gif.py -i 图片目录 -o 输出文件名.gif -d 帧延迟(毫秒)
   例如: python gif.py -i ./images -o output.gif -d 200

2. 导入为模块使用:
   from gif import create_gif
   create_gif(['图片1.png', '图片2.png'], 'output.gif', 200)
'''

import os
import argparse
import tempfile
import shutil
import math
from PIL import Image
import glob

# 用于处理视频文件
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("警告: 未安装opencv-python库，视频处理功能将不可用。请使用 'pip install opencv-python' 安装。")

def resize_images(image_list, target_size=None, keep_aspect_ratio=True, fill_mode='fill'):
    """
    将图片列表中的所有图片调整为统一大小
    
    参数:
        image_list: 图片文件路径列表
        target_size: 目标大小，格式为(宽, 高)。如果为None，则使用第一张图片的大小
        keep_aspect_ratio: 是否保持原始宽高比
        fill_mode: 填充模式，可选值：
            - 'center': 居中放置，周围可能有透明区域
            - 'fill': 缩放并裁剪，确保填满整个画面
    
    返回:
        list: 调整大小后的Image对象列表
    """
    if not image_list:
        return []
    
    # 如果没有指定目标大小，使用第一张图片的大小
    if target_size is None:
        first_img = Image.open(image_list[0])
        target_size = first_img.size
    
    resized_images = []
    for img_path in image_list:
        try:
            img = Image.open(img_path)
            
            if keep_aspect_ratio:
                if fill_mode == 'center':
                    # 保持宽高比的调整大小，居中放置
                    img.thumbnail(target_size, Image.Resampling.LANCZOS)
                    # 创建一个新的透明背景图像
                    new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
                    # 将调整后的图像粘贴到中心位置
                    paste_x = (target_size[0] - img.width) // 2
                    paste_y = (target_size[1] - img.height) // 2
                    new_img.paste(img, (paste_x, paste_y))
                    resized_images.append(new_img)
                elif fill_mode == 'fill':
                    # 保持宽高比但确保填满整个画面（可能会裁剪部分内容）
                    # 计算宽高比
                    target_ratio = target_size[0] / target_size[1]
                    img_ratio = img.width / img.height
                    
                    if img_ratio > target_ratio:
                        # 图片较宽，以高度为准进行缩放，然后裁剪宽度
                        new_height = target_size[1]
                        new_width = int(new_height * img_ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        # 裁剪中心部分
                        left = (new_width - target_size[0]) // 2
                        img = img.crop((left, 0, left + target_size[0], new_height))
                    else:
                        # 图片较高，以宽度为准进行缩放，然后裁剪高度
                        new_width = target_size[0]
                        new_height = int(new_width / img_ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        # 裁剪中心部分
                        top = (new_height - target_size[1]) // 2
                        img = img.crop((0, top, new_width, top + target_size[1]))
                    
                    resized_images.append(img)
            else:
                # 不保持宽高比，直接调整到目标大小
                resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                resized_images.append(resized_img)
                
        except Exception as e:
            print(f"调整图片 {img_path} 大小时出错: {e}")
    
    return resized_images

def create_gif_with_resize(image_list, output_file, duration=100, target_size=None, keep_aspect_ratio=True, fill_mode='fill'):
    """
    将多张图片调整为统一大小后合并成一张GIF动态图片
    
    参数:
        image_list: 图片文件路径列表
        output_file: 输出的GIF文件路径
        duration: 每一帧的延迟时间，单位为毫秒
        target_size: 目标大小，格式为(宽, 高)。如果为None，则使用第一张图片的大小
        keep_aspect_ratio: 是否保持原始宽高比
    
    返回:
        bool: 是否成功创建GIF
    """
    try:
        # 调整所有图片大小
        resized_images = resize_images(image_list, target_size, keep_aspect_ratio, fill_mode)
        
        if not resized_images:
            print("错误: 没有有效的图片可以处理")
            return False
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        # 保存为GIF
        resized_images[0].save(
            output_file,
            format='GIF',
            append_images=resized_images[1:],
            save_all=True,
            duration=duration,  # 毫秒
            loop=0  # 0表示无限循环
        )
        
        print(f"成功创建GIF: {output_file}")
        return True
    
    except Exception as e:
        print(f"创建GIF时出错: {e}")
        return False

def create_gif(image_list, output_file, duration=100):
    """
    将多张图片合并成一张GIF动态图片
    
    参数:
        image_list: 图片文件路径列表，或者已经打开的Image对象列表
        output_file: 输出的GIF文件路径
        duration: 每一帧的延迟时间，单位为毫秒
    
    返回:
        bool: 是否成功创建GIF
    """
    try:
        # 检查image_list是文件路径还是Image对象
        frames = []
        for item in image_list:
            if isinstance(item, str):
                # 如果是文件路径，打开图片
                img = Image.open(item)
                frames.append(img)
            elif isinstance(item, Image.Image):
                # 如果已经是Image对象，直接添加
                frames.append(item)
            else:
                print(f"警告: 忽略不支持的项目类型: {type(item)}")
        
        # 确保至少有一张图片
        if not frames:
            print("错误: 没有有效的图片可以处理")
            return False
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        # 保存为GIF
        frames[0].save(
            output_file,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=duration,  # 毫秒
            loop=0  # 0表示无限循环
        )
        
        print(f"成功创建GIF: {output_file}")
        return True
    
    except Exception as e:
        print(f"创建GIF时出错: {e}")
        return False

def create_gif_from_directory(input_dir, output_file, duration=100, pattern="*.png", resize=False, target_size=None, keep_aspect_ratio=True, fill_mode='fill'):
    """
    从指定目录读取所有图片并创建GIF
    
    参数:
        input_dir: 输入图片所在的目录
        output_file: 输出的GIF文件路径
        duration: 每一帧的延迟时间，单位为毫秒
        pattern: 文件匹配模式，默认为"*.png"
    
    返回:
        bool: 是否成功创建GIF
    """
    # 获取目录中所有匹配的图片
    image_paths = sorted(glob.glob(os.path.join(input_dir, pattern)))
    
    if not image_paths:
        print(f"错误: 在目录 {input_dir} 中没有找到匹配 {pattern} 的图片")
        return False
    
    print(f"找到 {len(image_paths)} 张图片")
    
    # 根据是否需要调整大小选择不同的处理函数
    if resize:
        return create_gif_with_resize(image_paths, output_file, duration, target_size, keep_aspect_ratio, fill_mode)
    else:
        return create_gif(image_paths, output_file, duration)

def extract_frames_from_video(video_path, start_time=0, end_time=None, fps=10, target_size=None, keep_aspect_ratio=True, fill_mode='fill'):
    """
    从视频文件中提取帧并返回图像列表
    
    参数:
        video_path: 视频文件路径
        start_time: 开始时间（秒）
        end_time: 结束时间（秒），如果为None则提取到视频结束
        fps: 每秒提取的帧数
        target_size: 目标大小，格式为(宽, 高)
        keep_aspect_ratio: 是否保持原始宽高比
    
    返回:
        list: 提取的帧（Image对象）列表
    """
    if not OPENCV_AVAILABLE:
        print("错误: 未安装opencv-python库，无法处理视频文件。请使用 'pip install opencv-python' 安装。")
        return []
    
    try:
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"错误: 无法打开视频文件 {video_path}")
            return []
        
        # 获取视频信息
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / video_fps if video_fps > 0 else 0
        
        # 如果未指定结束时间，则使用视频总时长
        if end_time is None or end_time > video_duration:
            end_time = video_duration
        
        # 计算需要提取的帧
        start_frame = int(start_time * video_fps)
        end_frame = int(end_time * video_fps)
        
        # 计算提取间隔（每隔多少帧提取一帧）
        if fps >= video_fps:
            # 如果请求的fps大于等于视频fps，则提取所有帧
            interval = 1
        else:
            # 否则按比例提取
            interval = int(video_fps / fps)
        
        print(f"视频信息: {video_duration:.2f}秒, {video_fps:.2f}fps, 总帧数: {total_frames}")
        print(f"提取设置: {start_time}秒 到 {end_time}秒, 输出{fps}fps, 提取间隔: {interval}帧")
        
        # 设置起始位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        frame_count = 0
        extracted_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret or frame_count > (end_frame - start_frame):
                break
            
            # 按间隔提取帧
            if frame_count % interval == 0:
                # 转换BGR到RGB（OpenCV使用BGR，PIL使用RGB）
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                
                # 如果需要调整大小
                if target_size:
                    if keep_aspect_ratio:
                        if fill_mode == 'center':
                            # 保持宽高比，居中放置
                            pil_img.thumbnail(target_size, Image.Resampling.LANCZOS)
                            # 创建新的透明背景
                            new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
                            # 居中粘贴
                            paste_x = (target_size[0] - pil_img.width) // 2
                            paste_y = (target_size[1] - pil_img.height) // 2
                            new_img.paste(pil_img, (paste_x, paste_y))
                            pil_img = new_img
                        elif fill_mode == 'fill':
                            # 保持宽高比但确保填满整个画面
                            # 计算宽高比
                            target_ratio = target_size[0] / target_size[1]
                            img_ratio = pil_img.width / pil_img.height
                            
                            if img_ratio > target_ratio:
                                # 图片较宽，以高度为准进行缩放，然后裁剪宽度
                                new_height = target_size[1]
                                new_width = int(new_height * img_ratio)
                                pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                                # 裁剪中心部分
                                left = (new_width - target_size[0]) // 2
                                pil_img = pil_img.crop((left, 0, left + target_size[0], new_height))
                            else:
                                # 图片较高，以宽度为准进行缩放，然后裁剪高度
                                new_width = target_size[0]
                                new_height = int(new_width / img_ratio)
                                pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                                # 裁剪中心部分
                                top = (new_height - target_size[1]) // 2
                                pil_img = pil_img.crop((0, top, new_width, top + target_size[1]))
                    else:
                        # 直接调整大小
                        pil_img = pil_img.resize(target_size, Image.Resampling.LANCZOS)
                
                frames.append(pil_img)
                extracted_count += 1
                
                # 显示进度
                if extracted_count % 10 == 0:
                    print(f"已提取 {extracted_count} 帧...")
            
            frame_count += 1
        
        cap.release()
        print(f"共提取 {len(frames)} 帧")
        return frames
    
    except Exception as e:
        print(f"提取视频帧时出错: {e}")
        return []

def create_gif_from_video(video_path, output_file, start_time=0, end_time=None, fps=10, duration=None, target_size=None, keep_aspect_ratio=True, fill_mode='fill'):
    """
    从视频文件创建GIF
    
    参数:
        video_path: 视频文件路径
        output_file: 输出的GIF文件路径
        start_time: 开始时间（秒）
        end_time: 结束时间（秒），如果为None则提取到视频结束
        fps: 每秒提取的帧数
        duration: 每一帧的延迟时间（毫秒），如果为None则根据fps自动计算
        target_size: 目标大小，格式为(宽, 高)
        keep_aspect_ratio: 是否保持原始宽高比
    
    返回:
        bool: 是否成功创建GIF
    """
    # 提取视频帧
    frames = extract_frames_from_video(video_path, start_time, end_time, fps, target_size, keep_aspect_ratio, fill_mode)
    
    if not frames:
        print("错误: 没有从视频中提取到有效帧")
        return False
    
    # 如果未指定duration，则根据fps计算
    if duration is None:
        duration = int(1000 / fps)  # 将fps转换为毫秒延迟
    
    # 创建GIF
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        # 保存为GIF
        frames[0].save(
            output_file,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=duration,  # 毫秒
            loop=0  # 0表示无限循环
        )
        
        print(f"成功创建GIF: {output_file}")
        return True
    
    except Exception as e:
        print(f"创建GIF时出错: {e}")
        return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将多张图片或视频片段合并成GIF动态图片')
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 从图片创建GIF的子命令
    img_parser = subparsers.add_parser('images', help='从图片创建GIF')
    img_parser.add_argument('-i', '--input', required=True, help='输入图片目录')
    img_parser.add_argument('-o', '--output', required=True, help='输出GIF文件路径')
    img_parser.add_argument('-d', '--duration', type=int, default=100, help='每一帧的延迟时间(毫秒)，默认100')
    img_parser.add_argument('-p', '--pattern', default='*.png', help='文件匹配模式，默认为"*.png"')
    img_parser.add_argument('-r', '--resize', action='store_true', help='是否调整图片大小')
    img_parser.add_argument('-w', '--width', type=int, help='调整后的图片宽度')
    img_parser.add_argument('--height', type=int, help='调整后的图片高度')
    img_parser.add_argument('-k', '--keep-aspect-ratio', action='store_true', default=True, help='是否保持原始宽高比')
    img_parser.add_argument('--fill-mode', choices=['center', 'fill'], default='fill', help='填充模式，当保持宽高比时：center=居中放置，fill=缩放裁剪填满画面（默认）')
    
    # 从视频创建GIF的子命令
    video_parser = subparsers.add_parser('video', help='从视频创建GIF')
    video_parser.add_argument('-i', '--input', required=True, help='输入视频文件路径')
    video_parser.add_argument('-o', '--output', required=True, help='输出GIF文件路径')
    video_parser.add_argument('-s', '--start', type=float, default=0, help='开始时间(秒)，默认0')
    video_parser.add_argument('-e', '--end', type=float, help='结束时间(秒)，默认为视频结束')
    video_parser.add_argument('-f', '--fps', type=float, default=10, help='每秒提取的帧数，默认10')
    video_parser.add_argument('-d', '--duration', type=int, help='每一帧的延迟时间(毫秒)，默认根据fps自动计算')
    video_parser.add_argument('-r', '--resize', action='store_true', help='是否调整图片大小')
    video_parser.add_argument('-w', '--width', type=int, help='调整后的图片宽度')
    video_parser.add_argument('--height', type=int, help='调整后的图片高度')
    video_parser.add_argument('-k', '--keep-aspect-ratio', action='store_true', default=True, help='是否保持原始宽高比')
    video_parser.add_argument('--fill-mode', choices=['center', 'fill'], default='fill', help='填充模式，当保持宽高比时：center=居中放置，fill=缩放裁剪填满画面（默认）')
    
    args = parser.parse_args()
    
    # 如果没有指定子命令，默认使用images命令（向后兼容）
    if not args.command:
        print("未指定命令，默认使用'images'命令处理图片目录")
        args.command = 'images'
        
        # 为兼容旧版本，检查是否提供了必要的参数
        if not hasattr(args, 'input') or not hasattr(args, 'output'):
            parser.print_help()
            return
    
    # 设置目标大小
    target_size = None
    if hasattr(args, 'width') and hasattr(args, 'height') and args.width and args.height:
        target_size = (args.width, args.height)
    
    # 根据命令执行相应的操作
    if args.command == 'images':
        # 从图片创建GIF
        fill_mode = getattr(args, 'fill_mode', 'fill')  # 兼容旧版本
        create_gif_from_directory(
            args.input, 
            args.output, 
            args.duration, 
            args.pattern, 
            args.resize, 
            target_size, 
            args.keep_aspect_ratio,
            fill_mode
        )
    elif args.command == 'video':
        # 从视频创建GIF
        if not OPENCV_AVAILABLE:
            print("错误: 未安装opencv-python库，无法处理视频文件。请使用 'pip install opencv-python' 安装。")
            return
        
        fill_mode = getattr(args, 'fill_mode', 'fill')  # 兼容旧版本
        create_gif_from_video(
            args.input,
            args.output,
            args.start,
            args.end,
            args.fps,
            args.duration,
            target_size,
            args.keep_aspect_ratio,
            fill_mode
        )

if __name__ == "__main__":
    main()
