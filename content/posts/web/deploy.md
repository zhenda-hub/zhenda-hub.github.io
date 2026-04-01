+++
title = 'Deploy'
subtitle = ""
date = 2026-03-27T00:17:14+08:00
draft = true
toc = true
series = []
+++

## 网站部署

Nginx

Docker + Gunicorn/Uvicorn

多个服务， 负载均衡（可以用nginx， 用户请求入口）
Nginx 只负责“用户层面的流量”，即：前端网页 + 后端 API

### 公共服务, 一起安装起来

```bash
pythono manage.py check --deploy
```

使用docker compose 配置 uwsgi 或者 gunicore

### 端口管理：

只需要暴露Nginx的80和443端口到主机。
Django应用和数据库的端口不需要对外暴露

| ip  | 作用      |
| --- | --------- |
| 80  | HTTP服务  |
| 443 | HTTPS服务 |
| 22  | SSH服务   |

### 多实例多进程

需要负载均衡
部署复杂
要处理：
session
数据一致性

👉 多进程解决：

“这台机器用不满”

👉 多实例解决：

“一台机器不够用”

通过Docker + 一个Nginx（或Cloudflare）来统一管理。

## Caddy

优点：配置少、自动SSL、无需手动处理证书、容易维护。
缺点：高级限流或缓存配置不如 Nginx 灵活（但你有 Cloudflare，完全够用）。

## Nginx Proxy Manager

## nginx

### why nginx

nginx : Nginx 反向代理（处理静态文件、限流、拦截攻击

反向代理:

后端服务器通常运行在内网环境。使用反向代理后，你只需要向互联网暴露一个 80/443 端口。黑客无法知道你后端服务器的具体 IP 或真实端口，这大大降低了被直接攻击的风险。

无缝部署（零停机更新）:可以先起一个新版本，让代理切过去，再关掉旧版本，用户感知不到任何波动。

在一个Nginx配置文件里写5个 server {} 块，每个对应一个域名

公网IP:80
↓
Nginx（唯一入口）
↓
┌───────────────┐
│ web1 (8001) │
│ web2 (8002) │
│ web3 (8003) │
│ web4 (8004) │
│ web5 (8005) │
└───────────────┘

不靠域名区分，靠「端口」或「子路径」区分 5 个网站:

只用服务器 IP + 不同端口，比如：
网站 1：http://你的服务器IP:81
网站 2：http://你的服务器IP:82
网站 3：http://你的服务器IP:83

用 路径区分（推荐）

http://你的IP/site1
http://你的IP/site2
http://你的IP/site3

### 配置

简化版

```txt
server {
    listen 80;

    # 限流（核心）
    limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;

    location / {
        limit_req zone=api burst=10 nodelay;
    }

    # 网站1
    location /site1/ {
        proxy_pass http://web1:8000/;
    }

    # 网站2
    location /site2/ {
        proxy_pass http://web2:8000/;
    }

    # 防路径穿越（你刚遇到的）
    if ($request_uri ~ "\.\.") {
        return 403;
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
}
```

```txt
# 基础代理配置（支持Cloudflare）
server {
    listen 80;
    server_name site1.com www.site1.com;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://localhost:3000; # 后端服务
    }

    # 静态资源缓存（加速访问）
    location ~* \.(css|js|png|jpg|gif)$ {
        expires 365d;
        add_header Cache-Control "public, immutable";
    }

    # 关键：API路径速率限制
    location /api/ {
        limit_req zone=api_limit burst=5 nodelay;
        limit_req_status 429;
        proxy_pass http://backend;
    }
}

# 创建速率限制区域（http块中）
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=1r/s;
```

```txt

# 拦路径穿越
if ($request_uri ~ "\.\.") {
    return 403;
}

# 禁止访问隐藏文件
location ~ /\. {
    deny all;
}


# 全局安全规则（所有网站通用，只写1次）
limit_req_zone $binary_remote_addr zone=api:10m rate=15r/s;
# 避免暴露Nginx版本
server_tokens off;

map $request_uri $bad_request {
    default 0;
    ~*\.\./ 1;
    ~*%2e%2e 1;
    ~*\/etc\/ 1;
    ~*\.env 1;
}

# 网站1
server {
    listen 81; # 端口81
    if ($bad_request) { return 403; }
    limit_req zone=api burst=5 nodelay;
    autoindex off;
    location / {
        proxy_pass http://127.0.0.1:8001; # 你的Django/FastAPI端口
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 网站2
server {
    listen 82; # 端口82
    if ($bad_request) { return 403; }
    limit_req zone=api burst=5 nodelay;
    autoindex off;
    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

```

```txt
http {
    # 限流：1秒20次请求
    limit_req_zone $binary_remote_addr zone=one:10m rate=20r/s;

    server_tokens off; # 隐藏版本，安全一点

    # 拦截目录遍历攻击
    map $request_uri $attack {
        default 0;
        ~*\.\./|%2e%2e|\.env|\/etc\/ 1;
    }

    # -------------------- 网站1 --------------------
    server {
        listen 80;
        server_name site1.你的域名.com;

        if ($attack) { return 403; }
        limit_req zone=one burst=5;

        location / {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
        }
    }

    # -------------------- 网站2 --------------------
    server {
        listen 80;
        server_name site2.你的域名.com;

        if ($attack) { return 403; }
        limit_req zone=one burst=5;

        location / {
            proxy_pass http://127.0.0.1:8002;
            proxy_set_header Host $host;
        }
    }

    # 网站3、4、5 复制上面这段，改域名和端口即可
}
```

```bash
nginx -t   # 测试配置
systemctl restart nginx
```

如果有cdn, 必须配置real_ip

### 性能

gzip on;
keepalive_timeout 65;

## 后续升级

### 升级到 Cloudflare（CDN + WAF）

当你：

有域名
流量变大
被攻击明显变多

### 升级多实例

当你：

CPU 不够
服务卡顿

### 升级日志系统(json日志)

当你：

查问题困难
有多服务器
