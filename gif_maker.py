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
from PIL import Image
import glob

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

def create_gif_from_directory(input_dir, output_file, duration=100, pattern="*.png"):
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
    return create_gif(image_paths, output_file, duration)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将多张图片合并成GIF动态图片')
    parser.add_argument('-i', '--input', required=True, help='输入图片目录')
    parser.add_argument('-o', '--output', required=True, help='输出GIF文件路径')
    parser.add_argument('-d', '--duration', type=int, default=100, help='每一帧的延迟时间(毫秒)，默认100')
    parser.add_argument('-p', '--pattern', default='*.png', help='文件匹配模式，默认为"*.png"')
    
    args = parser.parse_args()
    
    # 创建GIF
    create_gif_from_directory(args.input, args.output, args.duration, args.pattern)

if __name__ == "__main__":
    main()
