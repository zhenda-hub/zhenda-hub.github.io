+++
title = 'Ai Tool'
subtitle = ""
date = 2024-11-13T21:08:52+08:00
draft = false
toc = true
series = ['AI']
+++

[toc]

## cuda

```cmd
nvcc -V
```

```cmd
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Tue_Mar__8_18:36:24_Pacific_Standard_Time_2022
Cuda compilation tools, release 11.6, V11.6.124
Build cuda_11.6.r11.6/compiler.31057947_0

```


## ollama

本地大模型工具

- <https://ollama.com/>
- <https://github.com/ollama/ollama/blob/main/docs/api.md>
- <https://blog.csdn.net/asd54090/article/details/140775636>

```bash

ollama list
ollama ps

ollama run xxx
ollama pull xxx
ollama show xxx
ollama rm xxx
```

restful api

```bash

curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "The sky is blue because of Rayleigh scattering"
}'


curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'

curl http://localhost:11434/api/generate -d '{
  "model": "glm4",
  "prompt": "天空是什么颜色?",
  "stream": false
}'


```

容器访问ollama的地址

```
http://host.docker.internal:11434
```
