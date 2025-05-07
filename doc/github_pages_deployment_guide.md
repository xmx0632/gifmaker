# GitHub Pages 部署指南

本指南将帮助您将 GifMaker 项目网站部署到 GitHub Pages，让您的项目网站可以通过互联网访问。

## 目录

- [前提条件](#前提条件)
- [部署步骤](#部署步骤)
- [自定义域名设置](#自定义域名设置)
- [常见问题解决](#常见问题解决)
- [优化建议](#优化建议)

## 前提条件

在开始部署之前，请确保您已经：

1. 拥有一个 GitHub 账户
2. 已将 GifMaker 项目代码推送到 GitHub 仓库
3. 拥有仓库的管理权限

## 部署步骤

### 1. 准备您的仓库

确保您的仓库中包含网站所需的所有文件，特别是 `index.html` 文件，这是 GitHub Pages 默认的入口页面。GifMaker 项目已经包含了一个设计精美的 `index.html` 文件，可以直接用于部署。

### 2. 启用 GitHub Pages

1. 登录您的 GitHub 账户
2. 导航到您的 GifMaker 仓库页面
3. 点击仓库页面顶部的 "Settings" 选项卡
4. 在左侧菜单中，滚动并找到 "Pages" 选项
5. 在 "Source" 部分，从下拉菜单中选择分支（通常是 `main` 或 `master`）
6. 选择根目录 `/` 作为发布源
7. 点击 "Save" 按钮

![GitHub Pages 设置](https://docs.github.com/assets/images/help/pages/select-gh-pages-or-master-as-source.png)

### 3. 等待部署完成

启用 GitHub Pages 后，GitHub 将开始构建您的网站。这个过程通常需要几分钟时间。您可以在仓库的 "Actions" 选项卡中查看部署进度。

### 4. 访问您的网站

部署完成后，您将在 GitHub Pages 设置页面看到一个绿色的成功消息，其中包含您网站的 URL。默认情况下，URL 格式为：

```
https://<username>.github.io/<repository-name>/
```

例如，如果您的 GitHub 用户名是 "xmx0632"，仓库名是 "gifmaker"，那么您的网站 URL 将是：

```
https://xmx0632.github.io/gifmaker/
```

点击此链接即可访问您部署的 GifMaker 网站。

## 自定义域名设置

如果您希望使用自己的域名而不是默认的 github.io 域名，可以按照以下步骤设置：

### 1. 添加自定义域名

1. 在 GitHub 仓库的 "Settings" > "Pages" 页面
2. 在 "Custom domain" 部分，输入您的域名（例如 `gifmaker.yourdomain.com`）
3. 点击 "Save" 按钮

### 2. 配置 DNS 记录

您需要在您的域名注册商处添加 DNS 记录，将您的域名指向 GitHub Pages 服务器：

- 如果使用子域名（如 `gifmaker.yourdomain.com`），添加一个 CNAME 记录，指向 `<username>.github.io`
- 如果使用顶级域名（如 `yourdomain.com`），添加 A 记录，指向 GitHub Pages 的 IP 地址：
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153

### 3. 验证域名

添加 DNS 记录后，返回 GitHub Pages 设置页面，确认域名已被验证（通常会显示一个绿色的勾号）。

## 常见问题解决

### 网站无法访问

- 确认 GitHub Pages 已成功启用
- 检查是否选择了正确的分支和目录
- 查看 Actions 选项卡中是否有构建错误
- 确保仓库中存在 `index.html` 文件

### 样式或图片无法加载

- 检查 HTML 文件中的资源路径是否正确
- 确保使用相对路径而不是绝对路径
- 对于 GifMaker 项目，确保 `doc/cover.png` 等资源文件存在于仓库中

### 自定义域名问题

- DNS 记录可能需要 24-48 小时才能完全生效
- 确保 DNS 记录配置正确
- 检查是否在仓库中自动创建了 `CNAME` 文件

## 优化建议

### 1. 添加 README 链接

在您的 README.md 文件中添加网站链接，方便用户直接访问：

```markdown
## 在线演示

访问我们的[在线演示网站](https://xmx0632.github.io/gifmaker/)查看 GifMaker 的功能和特点。
```

### 2. 优化加载速度

- 压缩图片和 GIF 文件大小
- 考虑使用 CDN 加载第三方库
- 添加适当的缓存控制头

### 3. 添加 SEO 元标签

在 `index.html` 的 `<head>` 部分添加 SEO 相关的元标签，提高搜索引擎可见性：

```html
<meta name="description" content="GifMaker - 一个简单免费的GIF制作工具，轻松将多张图片或视频片段合成为高质量的动态GIF">
<meta name="keywords" content="GIF制作,图片合成,视频转GIF,开源工具">
<meta name="author" content="xmx0632">
```

### 4. 设置 404 页面

创建一个自定义的 `404.html` 文件，当用户访问不存在的页面时提供友好的错误提示。

---

通过按照本指南的步骤操作，您可以轻松地将 GifMaker 项目部署到 GitHub Pages，让更多用户了解和使用您的工具。如果您在部署过程中遇到任何问题，请参考 [GitHub Pages 官方文档](https://docs.github.com/cn/pages) 或在项目仓库中提出 issue。