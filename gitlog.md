# Git Commit Log

## 2025-03-04
docs(readme): 调整文档格式，优化图片和代码块的展示

- 调整 README.md 和 README_zh.md 中的代码块和图片排版
- 分离代码块和图片展示，提高可读性
- 保持中英文文档格式一致性

docs(readme): 在README中添加演示图片和视频

- 在 README.md 和 README_zh.md 中添加填充模式和居中模式的演示图片
- 添加视频转GIF的原始视频和生成结果的对比展示
- 优化命令行示例，增强文档的直观性

docs(license): 添加MIT许可证

- 创建 LICENSE 文件，采用 MIT 许可证
- 在 README.md 和 README_zh.md 中添加许可证声明
- 完善项目的法律文档

docs(readme): 添加赞赏码并优化文档展示

- 在 README.md 中添加支付宝和微信支付的赞赏码
- 使用 Markdown 表格将两个收款码并排展示
- 在 introduce.md 中添加演示图片和视频示例

feat(resize): 将fill模式设为默认选项

- 将 `fill-mode` 参数的默认值从 `center` 改为 `fill`
- 修改所有相关函数的默认参数
- 更新文档，将 `fill` 模式标记为默认选项
- 更新示例命令，反映新的默认行为

feat(resize): 添加图片填充模式功能

- 新增 `fill-mode` 参数，支持两种填充模式：`center`（居中放置）和`fill`（缩放裁剪填满）
- 修改 `resize_images` 函数，实现了新的填充模式逻辑
- 更新了视频帧提取函数，支持新的填充模式
- 更新命令行参数解析，增加 `--fill-mode` 参数
- 更新文档，添加新功能的说明和示例

docs(introduce): 更新公众号文章介绍文档

- 更新介绍文档，添加从视频创建GIF的新功能说明
- 更新命令行使用说明，增加视频模式的参数说明
- 调整文档结构，增加新功能的示例代码
- 更新产品特点和总结部分，突出视频转GIF功能

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
