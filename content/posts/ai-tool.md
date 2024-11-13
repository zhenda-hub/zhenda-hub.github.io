+++
title = 'Ai Tool'
subtitle = ""
date = 2024-11-13T21:08:52+08:00
draft = true
toc = true
tags = []
+++

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