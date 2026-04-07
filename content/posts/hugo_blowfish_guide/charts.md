+++
title = 'Blowfish 图表使用'
subtitle = '使用 Frontmatter 变量绘制图表'
date = 2025-04-07T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', 'Chart.js']
series = ['Hugo Blowfish 指南']

# 图表数据 - 柱状图
barChartLabels = ["一月", "二月", "三月", "四月", "五月", "六月"]
barChartValues = [65, 59, 80, 81, 56, 70]
barChartLabel = "月度活跃度"

# 图表数据 - 饼图
pieChartLabels = ["编程", "阅读", "写作", "运动", "其他"]
pieChartValues = [35, 20, 15, 20, 10]

# 图表数据 - 折线图
lineChartLabels = ["Week 1", "Week 2", "Week 3", "Week 4"]
lineChartValues1 = [12, 19, 15, 25]
lineChartValues2 = [8, 15, 12, 20]
+++

# Blowfish 图表使用

Blowfish 主题内置了 Chart.js 支持，可以通过 Frontmatter 变量灵活地管理图表数据。

## 为什么使用 Frontmatter 变量？

- **数据集中管理**：所有数据在文章开头定义，便于查看和修改
- **数据复用**：同一组数据可用于多个图表
- **维护方便**：更新数据时只需修改 frontmatter

## 使用 Frontmatter 管理图表数据

虽然 Hugo 不能直接在 `<script>` 标签中处理 frontmatter 变量，但你仍然可以在 frontmatter 中定义数据结构，然后复制到 shortcode 中使用。这样做的好处是：

- **数据集中管理**：所有数据在文章开头定义
- **便于维护**：修改数据时只需更新 frontmatter
- **结构清晰**：数据格式一目了然

### 在 Frontmatter 中定义数据

```toml
+++
# 图表数据参考
# 柱状图
barChartLabels = ["一月", "二月", "三月", "四月", "五月", "六月"]
barChartValues = [65, 59, 80, 81, 56, 70]
barChartLabel = "月度活跃度"

# 饼图
pieChartLabels = ["编程", "阅读", "写作", "运动", "其他"]
pieChartValues = [35, 20, 15, 20, 10]

# 折线图
lineChartLabels = ["Week 1", "Week 2", "Week 3", "Week 4"]
lineChartValues1 = [12, 19, 15, 25]
lineChartValues2 = [8, 15, 12, 20]
+++
```

### 使用数据创建图表

将 frontmatter 中定义的数据复制到 shortcode 中：

{{< chart >}}
type: 'bar',
data: {
  labels: ["一月", "二月", "三月", "四月", "五月", "六月"],
  datasets: [{
    label: "月度活跃度",
    data: [65, 59, 80, 81, 56, 70],
    backgroundColor: 'rgba(54, 162, 235, 0.8)',
    borderColor: 'rgb(54, 162, 235)',
    borderWidth: 1
  }]
}
{{< /chart >}}

## 图表示例

### 柱状图

{{< chart >}}
type: 'bar',
data: {
  labels: ["一月", "二月", "三月", "四月", "五月", "六月"],
  datasets: [{
    label: "月度活跃度",
    data: [65, 59, 80, 81, 56, 70],
    backgroundColor: 'rgba(54, 162, 235, 0.8)',
    borderColor: 'rgb(54, 162, 235)',
    borderWidth: 1
  }]
}
{{< /chart >}}

### 饼图

{{< chart >}}
type: 'doughnut',
data: {
  labels: ["编程", "阅读", "写作", "运动", "其他"],
  datasets: [{
    data: [35, 20, 15, 20, 10],
    backgroundColor: [
      'rgba(255, 99, 132, 0.8)',
      'rgba(54, 162, 235, 0.8)',
      'rgba(255, 206, 86, 0.8)',
      'rgba(75, 192, 192, 0.8)',
      'rgba(153, 102, 255, 0.8)'
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

### 折线图

{{< chart >}}
type: 'line',
data: {
  labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
  datasets: [
    {
      label: '项目 A',
      data: [12, 19, 15, 25],
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.3
    },
    {
      label: '项目 B',
      data: [8, 15, 12, 20],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      tension: 0.3
    }
  ]
}
{{< /chart >}}

## 高级技巧

### 使用多数据集

在一个图表中显示多个数据集：

{{< chart >}}
type: 'line',
data: {
  labels: ["一月", "二月", "三月", "四月", "五月", "六月"],
  datasets: [
    {
      label: '2024年',
      data: [65, 59, 80, 81, 56, 70],
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.3
    },
    {
      label: '2023年',
      data: [45, 49, 60, 71, 46, 50],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      tension: 0.3
    }
  ]
}
{{< /chart >}}

### 自定义图表选项

通过 `options` 参数自定义图表外观：

{{< chart >}}
type: 'bar',
data: {
  labels: ["A", "B", "C", "D"],
  datasets: [{
    label: '数据',
    data: [10, 20, 30, 40],
    backgroundColor: 'rgba(54, 162, 235, 0.8)'
  }]
},
options: {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true
    }
  },
  plugins: {
    legend: {
      display: true,
      position: 'top'
    }
  }
}
{{< /chart >}}

## 注意事项

1. **数据直接嵌入**：图表数据需要直接写在 shortcode 中，不能通过 JavaScript 动态读取 frontmatter
2. **推荐做法**：在 frontmatter 中定义数据作为参考，然后复制到 shortcode 中
3. **语法格式**：shortcode 使用 YAML 格式，注意引号和逗号
4. **性能考虑**：大量数据时考虑分页或简化图表

## 相关资源

- [Chart.js 官方文档](https://www.chartjs.org/docs/latest/)
- [Blowfish 图表示例](https://blowfish.page/samples/charts/)
- [Hugo jsonify 函数](https://gohugo.io/functions/jsonify/)
