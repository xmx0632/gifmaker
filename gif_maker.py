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
from PIL import Image
import glob

def resize_images(image_list, target_size=None, keep_aspect_ratio=True):
    """
    将图片列表中的所有图片调整为统一大小
    
    参数:
        image_list: 图片文件路径列表
        target_size: 目标大小，格式为(宽, 高)。如果为None，则使用第一张图片的大小
        keep_aspect_ratio: 是否保持原始宽高比
    
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
                # 保持宽高比的调整大小
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                # 创建一个新的白色背景图像
                new_img = Image.new("RGBA", target_size, (255, 255, 255, 0))
                # 将调整后的图像粘贴到中心位置
                paste_x = (target_size[0] - img.width) // 2
                paste_y = (target_size[1] - img.height) // 2
                new_img.paste(img, (paste_x, paste_y))
                resized_images.append(new_img)
            else:
                # 不保持宽高比，直接调整到目标大小
                resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                resized_images.append(resized_img)
                
        except Exception as e:
            print(f"调整图片 {img_path} 大小时出错: {e}")
    
    return resized_images

def create_gif_with_resize(image_list, output_file, duration=100, target_size=None, keep_aspect_ratio=True):
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
        resized_images = resize_images(image_list, target_size, keep_aspect_ratio)
        
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

def create_gif_from_directory(input_dir, output_file, duration=100, pattern="*.png", resize=False, target_size=None, keep_aspect_ratio=True):
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
        return create_gif_with_resize(image_paths, output_file, duration, target_size, keep_aspect_ratio)
    else:
        return create_gif(image_paths, output_file, duration)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将多张图片合并成GIF动态图片')
    parser.add_argument('-i', '--input', required=True, help='输入图片目录')
    parser.add_argument('-o', '--output', required=True, help='输出GIF文件路径')
    parser.add_argument('-d', '--duration', type=int, default=100, help='每一帧的延迟时间(毫秒)，默认100')
    parser.add_argument('-p', '--pattern', default='*.png', help='文件匹配模式，默认为"*.png"')
    parser.add_argument('-r', '--resize', action='store_true', help='是否调整图片大小')
    parser.add_argument('-w', '--width', type=int, help='调整后的图片宽度')
    parser.add_argument('--height', type=int, help='调整后的图片高度')
    parser.add_argument('-k', '--keep-aspect-ratio', action='store_true', default=True, help='是否保持原始宽高比')
    
    args = parser.parse_args()
    
    # 设置目标大小
    target_size = None
    if args.width and args.height:
        target_size = (args.width, args.height)
    
    # 创建GIF
    create_gif_from_directory(
        args.input, 
        args.output, 
        args.duration, 
        args.pattern, 
        args.resize, 
        target_size, 
        args.keep_aspect_ratio
    )

if __name__ == "__main__":
    main()
