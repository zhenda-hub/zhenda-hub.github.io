+++
title = '博客统计'
subtitle = "文章分类数据可视化"
date = 2024-01-01T00:00:00+08:00
draft = false
toc = true
tags = ['数据', '统计']
showDate = false
+++

## 文章分类统计

截至 2026 年 4 月，博客共收录 **109** 篇文章。

### 柱状图

{{< chart >}}
type: 'bar',
data: {
  labels: ['生活', '编程语言', '工具', '技术', 'Web', '系统', '社会', 'Hugo', '圣经', '视频', 'AI'],
  datasets: [{
    label: '文章数量',
    data: [16, 14, 13, 12, 11, 11, 8, 7, 7, 5, 5],
    backgroundColor: [
      'rgba(255, 99, 132, 0.6)',
      'rgba(54, 162, 235, 0.6)',
      'rgba(255, 206, 86, 0.6)',
      'rgba(75, 192, 192, 0.6)',
      'rgba(153, 102, 255, 0.6)',
      'rgba(255, 159, 64, 0.6)',
      'rgba(199, 199, 199, 0.6)',
      'rgba(83, 102, 255, 0.6)',
      'rgba(255, 99, 255, 0.6)',
      'rgba(54, 255, 132, 0.6)',
      'rgba(255, 132, 54, 0.6)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 206, 86)',
      'rgb(75, 192, 192)',
      'rgb(153, 102, 255)',
      'rgb(255, 159, 64)',
      'rgb(199, 199, 199)',
      'rgb(83, 102, 255)',
      'rgb(255, 99, 255)',
      'rgb(54, 255, 132)',
      'rgb(255, 132, 54)'
    ],
    borderWidth: 1
  }]
},
options: {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 2
      }
    }
  }
}
{{< /chart >}}

### 饼图

{{< chart >}}
type: 'doughnut',
data: {
  labels: ['生活', '编程语言', '工具', '技术', 'Web', '系统', '社会', 'Hugo', '圣经', '视频', 'AI'],
  datasets: [{
    data: [16, 14, 13, 12, 11, 11, 8, 7, 7, 5, 5],
    backgroundColor: [
      'rgba(255, 99, 132, 0.8)',
      'rgba(54, 162, 235, 0.8)',
      'rgba(255, 206, 86, 0.8)',
      'rgba(75, 192, 192, 0.8)',
      'rgba(153, 102, 255, 0.8)',
      'rgba(255, 159, 64, 0.8)',
      'rgba(199, 199, 199, 0.8)',
      'rgba(83, 102, 255, 0.8)',
      'rgba(255, 99, 255, 0.8)',
      'rgba(54, 255, 132, 0.8)',
      'rgba(255, 132, 54, 0.8)'
    ],
    borderWidth: 0,
    hoverOffset: 10
  }]
},
options: {
  responsive: true,
  plugins: {
    legend: {
      position: 'right'
    }
  }
}
{{< /chart >}}

## 分类说明

| 分类 | 文章数 | 描述 |
|------|--------|------|
| life | 16 | 生活记录、健康管理 |
| programming_language | 14 | Python, Go, JS, TS 等编程语言 |
| tools | 13 | Git, Excel, PPT, IDE 等工具使用 |
| tech | 12 | 技术、架构、数据库 |
| web | 11 | Web 开发框架、爬虫、部署 |
| system | 11 | Linux, Windows, 服务器配置 |
| social | 8 | 社会观察、商业思考 |
| hugo_guide | 7 | Hugo 静态博客教程 |
| bible_stu | 7 | 圣经学习、神学 |
| videos | 5 | 视频笔记、影视推荐 |
| ai | 5 | AI 工具、教程 |
