#!/bin/bash
# 激活虚拟环境的脚本

echo "正在激活虚拟环境..."
source venv/bin/activate

echo "虚拟环境已激活！"
echo "Python 版本: $(python --version)"
echo "当前工作目录: $(pwd)"
echo ""
echo "要退出虚拟环境，请输入: deactivate"
echo "要运行应用，请输入: python app.py"
