#!/bin/bash
# 发布新版本的脚本

# 检查是否提供了版本号
if [ -z "$1" ]; then
  echo "错误: 请提供版本号"
  echo "用法: ./release.sh 1.0.0"
  exit 1
fi

VERSION="v$1"

# 确保工作目录干净
if [ -n "$(git status --porcelain)" ]; then
  echo "错误: 工作目录不干净，请先提交或暂存所有更改"
  exit 1
fi

# 创建标签
echo "创建标签 $VERSION..."
git tag -a "$VERSION" -m "发布版本 $VERSION"

# 推送标签到远程仓库
echo "推送标签到远程仓库..."
git push origin "$VERSION"

echo "标签 $VERSION 已创建并推送到远程仓库"
echo "GitHub Actions 将自动构建并发布此版本"
echo "请访问 GitHub 仓库的 Actions 页面查看构建进度"
