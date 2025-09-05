#!/bin/bash

# Cash Admin 启动脚本

echo "╔══════════════════════════════════════╗"
echo "║          Cash Admin 启动脚本         ║"
echo "╚══════════════════════════════════════╝"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 检测到虚拟环境: $VIRTUAL_ENV"
else
    echo "⚠️  建议在虚拟环境中运行"
fi

# 检查依赖是否安装
echo "🔍 检查依赖..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
else
    echo "✅ 依赖已安装"
fi

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 配置文件"
    echo "📝 创建默认配置文件..."
    cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
GAME_SERVER_URL=http://localhost:5000
GAME_SERVER_ADMIN_KEY=admin-key
EOF
    echo "✅ 已创建默认配置文件 .env"
    echo "⚠️  请根据需要修改 .env 文件中的配置"
fi

# 启动应用
echo ""
echo "🚀 启动 Cash Admin..."
echo "📍 访问地址: http://localhost:5001"
echo "⏹️  按 Ctrl+C 停止服务"
echo ""

python3 run.py
