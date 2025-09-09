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

## RAG

<https://blog.csdn.net/weixin_43589681/article/details/139269119>

Q: RAG是什么?

A: RAG，全称Retrieval-Augmented Generation，中文译为检索增强生成。它是一种结合了信息检索和生成模型的技术，旨在让大语言模型（LLM）能够访问和利用外部知识库中的信息，从而生成更准确、更全面的回答。



rag步骤

| 步骤	    |  关键性	      |  为什么重要 |
|------------|---------------|---|
| 文本切分	| ⭐⭐⭐⭐⭐	  | 决定 chunk 的质量，影响检索和回答效果 |
| 嵌入模型	| ⭐⭐⭐⭐	    | 决定语义理解质量，影响相似度召回 |
| 问答逻辑	| ⭐⭐⭐	      |  决定 prompt 怎么写，能不能让 LLM 发挥最优 |
| 向量索引	| ⭐⭐	        |  标准化组件，只影响性能、可扩展性 |
| 文档加载	| ⭐	          |   一次性任务，只要能读出干净文本即可 |
| 调用模型	| ⭐	          |    技术细节，LLM 换哪个都行，影响较小 |


## cursor

```
curl i
```
