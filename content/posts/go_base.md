+++
title = 'Go_base'
subtitle = ""
date = 2024-09-25T17:17:57+08:00
draft = false
toc = true
tags = ["go"]
+++

## 资料

- <https://go.dev/doc/#references>
- <https://tour.go-zh.org/basics/1>
- <https://pkg.go.dev/std>

一个Go项目中只能有一个 main 包和一个 main() 函数

你会直接编辑 go.mod（虽然通常通过 Go 命令来做），但永远不应该手动编辑 go.sum
用于管理项目的依赖关系。它们共同保证了项目的构建过程的可靠性和可重复性

go 版本切换
-  gvm
-  asdf

## 命令

```bash
# 下载依赖
go mod init xxx
# 更新go.mod文件
go mod tidy
# 更新依赖
go get -u
go get .

go run .
# 打包main包
go build
go test xxx
# 使用 air 进行热重载
air
```

## 包管理

```bash
go get -u xxx
```

## 数据结构

变量

短赋值语句 := 可在隐式确定类型的 var 声明中使用, 不能在函数外使用

```go
/*
这是一个多行注释
可以用于注释多行内容
*/

// 单行注释

var i int
var f float64 = 3.14
name := "Alice" // 简短变量声明
```

类型转换
```go
var a int = 10
var b float64 = float64(a)
```

数组
```go
var arr [5]int = [5]int{1, 2, 3, 4, 5}
arr[2] = 10
```

slice
```go
var s []int = []int{1, 2, 3, 4}
s = append(s, 5)
```

map
```go
m := make(map[string]int)
m["age"] = 30
delete(m, "age")

```
pointer

```go
var x int = 10
var p *int = &x
fmt.Println(*p) // 输出 10
```

结构体

```go
type Person struct {
    Name string
    Age  int
}
```
## 控制逻辑

for
```go
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

for index, value := range arr {
    fmt.Println(index, value)
}
```

if
```go
if x > 10 {
    fmt.Println("x is greater than 10")
} else {
    fmt.Println("x is less than or equal to 10")
}
```

函数

```go
func greet(name string) {
    fmt.Printf("Hello, %s!\n", name)
}
```


interface

```go
type Animal interface {
    move()
    eat()
}
```

## 并发

并发模型基于 goroutine 和 channel
