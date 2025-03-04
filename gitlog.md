# Git Commit Log

## 2025-03-04
feat(video): 添加从视频文件提取片段制作GIF功能

- 新增从视频文件提取片段并制作GIF的功能
- 重构命令行参数解析，使用子命令模式（`images`和`video`）
- 添加视频处理相关参数：`-s/--start`、`-e/--end`、`-f/--fps`
- 更新README.md，添加视频处理功能的说明和使用示例
- 添加opencv-python依赖到requirements.txt
- 保持向后兼容性，支持旧版命令行格式

feat(resize): 添加图片大小调整功能

- 新增调整图片大小功能，支持将不同大小的图片调整为统一大小
- 添加相关命令行参数：`-r/--resize`、`-w/--width`、`--height`和`-k/--keep-aspect-ratio`
- 更新README.md，添加新功能说明和使用示例
- 新增产品介绍文档和封面图片
