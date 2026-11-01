# 雨落成海 · 首页改版预览

此目录中的改动只存在于 `design/editorial-homepage` 分支。线上发布分支为 `gh-pages`，不要直接合并或修改 Pages 发布来源。

## 本地预览（不会部署）

1. `git clone --branch design/editorial-homepage https://github.com/mistysigh/mistysigh.github.io.git`
2. `cd mistysigh.github.io`
3. `python3 -m http.server 8000`
4. 浏览器打开 `http://localhost:8000/`。

使用本地 HTTP 服务而非双击 HTML 文件，是为了让以 `/css/`、`/js/`、`/images/` 开头的资源路径正确加载。

## 已实现

- 首页中文品牌「雨落成海」、SVG Logo 与 SVG favicon
- 杂志式首页主视觉与品牌导航
- 真实现有笔记、生活记录的分类筛选与本页搜索
- 响应式布局、暗色模式和键盘焦点样式

## 发布前核验

- [ ] 桌面和手机端检查导航、内容卡片、搜索与分类筛选
- [ ] 检查亮色/暗色模式与键盘 Tab 导航
- [ ] 检查 `/notes/`、`/life/`、`/archives/`、`/about/` 的链接
- [ ] 查明 Hexo 源码与部署流水线：当前分支是静态生成结果，直接编辑 `index.html` 可能在下一次 Hexo 构建时被覆盖
- [ ] 如需公网预览，单独配置不指向 `gh-pages` 的预览部署（如独立预览项目）；本分支本身不会自动生成公网预览网址

注意：当前品牌只接入首页；文章页和栏目页仍保持旧站标题及图标。