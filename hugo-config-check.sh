#!/bin/bash

echo "== Hugo Configuration Check =="

# 检查Hugo版本
hugo version

# 检查内容目录
echo "Content directory:"
ls -R content

# 检查配置文件
echo "Configuration file:"
cat config.toml || cat config.yaml || cat config.json || echo "No config file found"

# 检查主题
echo "Theme directory:"
ls -R themes

# 尝试构建站点
echo "Attempting to build site:"
hugo --minify

echo "== End of Check =="