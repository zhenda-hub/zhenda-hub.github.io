+++
title = "About Hugo"
description = "Hugo, the world's fastest framework for building websites"
date = "2019-02-28"
aliases = ["about-us", "about-hugo", "contact"]
series = ["Themes Guide"]
author = "Hugo Authors"
+++

Written in Go, Hugo is an open source static site generator available under the [Apache Licence 2.0.](https://github.com/gohugoio/hugo/blob/master/LICENSE) Hugo supports TOML, YAML and JSON data file types, Markdown and HTML content files and uses shortcodes to add rich content. Other notable features are taxonomies, multilingual mode, image processing, custom output formats, HTML/CSS/JS minification and support for Sass SCSS workflows.

Hugo makes use of a variety of open source projects including:

-   https://github.com/yuin/goldmark
-   https://github.com/alecthomas/chroma
-   https://github.com/muesli/smartcrop
-   https://github.com/spf13/cobra
-   https://github.com/spf13/viper

Hugo is ideal for blogs, corporate websites, creative portfolios, online magazines, single page applications or even a website with thousands of pages.

Hugo is for people who want to hand code their own website without worrying about setting up complicated runtimes, dependencies and databases.

Websites built with Hugo are extremely fast, secure and can be deployed anywhere including, AWS, GitHub Pages, Heroku, Netlify and any other hosting provider.

Learn more and contribute on [GitHub](https://github.com/gohugoio).

## 内容总结

-   建站流程
    -   创建
        -   hugo new site xxx
        -   下载优质皮肤
            -   Hextra | Hugo Themes (gohugo.io)
            -   Doks | Hugo Themes (gohugo.io)
            -   Jane | Hugo Themes (gohugo.io)
            -   Hugoplate | Hugo Themes (gohugo.io)
            -   Puppet | Hugo Themes (gohugo.io)
            -   https://github.com/flysnow-org/maupassant-hugo
        -   调试
            -   hugo server
                -   -D
        -   修改配置文件
        -   hugo new
            -   content/posts/xx.md
                -   具体文件的路径
            -   生成带有图片的 md 的文件结构
                -   posts/first
                    -   first.md
                    -   imgs
                        -   1.jpg
                        -   2.jpg
    -   生成
        -   hugo
            -   -D
        -   生成的静态网站
            -   public
                -   关联 pages
                -   查看结构得出结论
                    -   static 内的文件直接生成在根目录
-   module

-   博客分类
    -   md 文件顶部，设置 tags=[]
-   头部导航栏固定
    -   fixed-top
