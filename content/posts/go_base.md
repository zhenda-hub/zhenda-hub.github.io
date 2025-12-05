+++
title = 'Go_base'
subtitle = ""
date = 2024-09-25T17:17:57+08:00
draft = false
toc = true
tags = ["go"]
+++

[toc]

## 资料

- <https://go.dev/doc/#references>
- <https://tour.go-zh.org/basics/1>
- <https://pkg.go.dev/std>

一个Go项目中只能有**一个 main 包和一个 main() 函数**

你会直接编辑 go.mod（虽然通常通过 Go 命令来做），但永远不应该手动编辑 go.sum
用于管理项目的依赖关系。它们共同保证了项目的构建过程的可靠性和可重复性

go 版本切换
-  gvm
-  asdf

## 命令

```bash
# 下载依赖
go mod init xxx
# 更新依赖
go get -u
go get .
# 更新go.mod文件
go mod tidy
# 查看依赖
go list -m all

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


## 常用工具包

| 包名           | 功能           | 常用函数                          |
| :------------- | :------------- | :-------------------------------- |
| fmt            | 格式化输入输出 | Println, Printf, Sprintf          |
| strings        | 字符串处理     | Split, Contains, Replace, ToLower |
| strconv        | 字符串转换     | Atoi, ParseInt, Itoa, FormatInt   |
| math           | 数学函数       | Max, Min, Sqrt, Pow, Abs          |
| os             | 操作系统接口   | Open, Create, ReadFile, WriteFile |
| io             | 输入输出接口   | Reader, Writer, Copy              |
| log            | 日志记录       | Println, Fatal, Panic             |
| time           | 时间处理       | Now, Sleep, Parse, Format         |
| sort           | 排序           | Ints, Strings, Sort, Reverse      |
| errors         | 错误处理       | New, Is, As                       |
| bufio          | 缓冲 I/O       | Scanner, Reader, Writer           |
| json           | JSON 处理      | Marshal, Unmarshal                |
| encoding/json | JSON 编码和解码 | Marshal, Unmarshal                |
| encoding/xml  | XML 编码和解码  | Marshal, Unmarshal                |
| encoding/csv  | CSV 编码和解码  | NewReader, NewWriter              |
| container/list | 链表           | New, PushBack, Remove             |
| container/heap | 堆             | Push, Pop, Init                   |
| net/http      | HTTP 客户端和服务器 | Get, Post, ListenAndServe         |
| net/url      | URL 解析和构建 | Parse, URL, QueryEscape          |
| context        | 上下文管理     | Background, WithCancel, WithTimeout |
| database/sql   | 数据库操作     | Open, Query, Exec                 |

```go
import (
    "fmt"
    "strings"
    "strconv"
    "math"
    "os"
    "io"
    "log"
    "time"
    "sort"
    "errors"
    "bufio"
    "encoding/json"
    "net/http"
    "context"
    "database/sql"
)

func main() {
    // 示例代码
    fmt.Println("Hello, Go!")
}

```

## 并发

并发模型基于 goroutine 和 channel
