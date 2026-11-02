# 雨落成海 · 独立预览与上线检查

## 在线预览（不影响线上站点）

- **预览网址**：https://raw.githack.com/mistysigh/mistysigh.github.io/editorial-preview/index.html
- 预览分支：`editorial-preview`，从 `design/editorial-homepage` 独立复制。
- 正式发布分支：`gh-pages`，本次操作没有修改。
- 开发分支：`design/editorial-homepage`，保留原本可用于未来整合的代码。

预览通过第三方 raw.githack.com 开发 CDN 直接载入公开 GitHub 文件，**并非 GitHub Pages 正式部署，也不是独立托管服务的保证可用发布**。它可能展示一次安全确认页面，并可能延迟数分钟反映最新提交。若浏览器报错，亦可尝试备用地址：

https://htmlpreview.github.io/?https://github.com/mistysigh/mistysigh.github.io/blob/editorial-preview/index.html

## 预览边界

- 只对首页应用新版视觉及筛选交互；学术笔记、生活记录等栏目链接跳转至既有正式站点。
- 预览分支中特设 `css/rain-brand-preview.css`、`js/rain-brand-preview.js`，把根路径资源修正为可跨站点加载的绝对网址。
- 保留了文档中所有有效文章链接，没有迁移或修改正式页面。
- 不要将 `editorial-preview` 配置为 mistysigh.github.io 的 GitHub Pages 发布源。
- 该服务可能出现缓存、浏览器安全限制或外部脚本资源限制；仓库文件存在性检查不等于已验证页面真实加载。

## 桌面和手机检查

- [ ] 电脑端检查云海横幅、书法 Logo、印章、导航、文章卡片布局
- [ ] 手机端检查导航菜单、标题缩放、水平溢出、横幅图片裁切
- [ ] 测试“全部 / 学术笔记 / 日常生活”的过滤
- [ ] 测试搜索框及“无匹配文章”提示
- [ ] 检查亮色/暗色模式与键盘 Tab 操作
- [ ] 检查控制台错误、第三方 CDN 字体和脚本加载
- [ ] 核对所有文章 URL，确认导航不会跳转至不存在的预览路径

## 仍需解决

正式上线前应找到原始 Hexo 源码仓库与部署流程，避免重新构建时覆盖静态页面改动。任何上线都应在完成桌面和手机实测之后单独确认。
