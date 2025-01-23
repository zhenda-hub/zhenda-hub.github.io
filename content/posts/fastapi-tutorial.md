+++
title = 'Fastapi Tutorial'
subtitle = ""
date = 2024-11-09T22:57:03+08:00
draft = true
toc = true
tags = ["web"]
+++

link <https://fastapi.tiangolo.com/zh/tutorial/first-steps/>

## 快速开始

```bash
uvicorn main:app --reload --port 8000
```

查看restful 文档:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## 前置内容

### 异步

async await


### pydantic 类型

<https://docs.pydantic.dev/latest/concepts/models/>
<https://docs.pydantic.dev/latest/examples/orms/#__tabbed_1_2>

Annotated 和 pydantic 结合:

```python
from typing import Annotated
from pydantic import BaseModel, Field

Annotated[str, Field(min_length=2, max_length=5)]
```

## view函数

### 请求参数和校验

```python
from pydantic import BaseModel, Field

app = FastAPI()


# 请求体定义
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
```

- Query
- Path
- Params
- Field

父类 FieldInfo

### 数据库模块

### 依赖注入

依赖注入系统非常简单。依赖注入无非是与路径操作函数一样的函数罢了。

Depends

```python
from typing import Union

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```
## 中间件

middleware

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 用户认证

## 后台任务

Celery 集成

## 组织项目

APIRouter

```python
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
```

```python
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

