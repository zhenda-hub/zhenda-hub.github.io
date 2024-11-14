+++
title = 'Ai Tool'
subtitle = ""
date = 2024-11-13T21:08:52+08:00
draft = false
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

容器访问ollama的地址

```
http://host.docker.internal:11434
```


## embedding

<https://blog.csdn.net/weixin_43589681/article/details/139269119>

Q: RAG是什么?

A: RAG，全称Retrieval-Augmented Generation，中文译为检索增强生成。它是一种结合了信息检索和生成模型的技术，旨在让大语言模型（LLM）能够访问和利用外部知识库中的信息，从而生成更准确、更全面的回答。



Q: 为什么需要 embedding?

A: embedding 是将文本、图像等非数值数据转化为**数值向量**的一种技术。在RAG中，embedding起到了至关重要的桥梁作用。

embedding的特点:

- 语义表达能力强:

Embedding 可以捕捉词汇和句子的语义信息。
相似的词语和句子在向量空间中也会相近。


- 模型输入优化:

大多数机器学习模型需要数值型输入,Embedding 可以将文本转换为合适的输入格式。


- 计算效率提升:

Embedding 可以大幅压缩文本信息,降低计算复杂度。
基于向量运算的模型计算效率更高。

