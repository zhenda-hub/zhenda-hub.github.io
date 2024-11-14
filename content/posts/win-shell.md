+++
title = 'Win Shell'
subtitle = ""
date = 2024-11-12T20:32:30+08:00
draft = false
toc = true
tags = []
+++

## powershell

### 自定义 

```powershell
notepad $PROFILE
```

编辑

```powershell
# 默认的别名
# Set-Alias pwd Get-Location
# Set-Alias ls Get-ChildItem
# Set-Alias cd Set-Location
# Set-Alias cat Get-Content
# Set-Alias cp Copy-Item
# Set-Alias rm Remove-Item
# Set-Alias mv Move-Item
# Set-Alias mkdir New-Item -ItemType Directory
# Set-Alias -Name clear -Value Clear-Host
# Set-Alias -Name history -Value Get-History




# Set-Alias -Name which -Value Get-Command

# 创建自定义函数
function touch {
    param (
        [string]$path
    )
    New-Item -ItemType File -Path $path -Force
}



# 进程/服务操作
Set-Alias -Name top -Value Get-Process
Set-Alias -Name kill -Value Stop-Process

# 网络操作
Set-Alias -Name ping -Value Test-Connection
Set-Alias -Name wget -Value Invoke-WebRequest
```

### 环境变量

```powershell
ls Env:
$Env:MY_VAR = "InitialValue"
$Env:MY_VAR
rm Env:MY_VAR


$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
```