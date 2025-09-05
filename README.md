# zhenda's blog

a project to generate my blog

## github actions

- <https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site>
- <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>

## 静态博客工具

- hugo
- hexo
- mkdocs

## hugo settings doc

- https://gohugo.io/getting-started/configuration-markup/
- https://lawsssscat.github.io/hugo-usage-doc/docs/hugo/layout-usage/
- https://gohugo.io/content-management/mathematics/

## install hugo

https://gohugo.io/installation/linux/

```bash
# install and update
brew install hugo
```

## theme

https://github.com/roninro/hugo-theme-puppet

### comments

use giscus:
- https://giscus.app/zh-CN
- https://blog.highp.ing/p/giscus/
- https://fengchao.pro/blog/comment-system-with-giscus/

## hugo multi theme

- Blowfish
- hextra
- Beautiful Hugo
- Coder
- PaperMod
- LoveIt

- Hugo Blox

- Zen
- DoIt
- Terminal
- Ananke
- Hugo Book
- Hermit
- Hemingway
- uBlogger




```bash
git submodule update --init --recursive # needed when you reclone your repo (submodules may not get cloned automatically)



git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

git submodule add https://github.com/luizdepra/hugo-coder.git themes/hugo-coder

git submodule add -b main https://github.com/nunocoracao/blowfish.git themes/blowfish

git submodule add https://github.com/halogenica/beautifulhugo.git themes/beautifulhugo

git submodule add https://github.com/imfing/hextra.git themes/hextra

git submodule add https://github.com/dillonzq/LoveIt.git themes/LoveIt

git submodule add https://github.com/zhenda-hub/hugo-theme-puppet.git themes/puppet_zd
```




```toml
theme = "主题名"
```


```bash
# 当使用CI/CD部署Hugo网站时，确保在运行hugo命令之前执行以下命令至关重要。
git submodule update --init
```



```bash
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1) 
Press Ctrl+C to stop
```

TODO: add series