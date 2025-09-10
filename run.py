#!/usr/bin/env python3
"""
Cash Admin 启动脚本
"""

import os
import sys
from app import create_app

def main():
    """主函数"""
    # 设置环境变量
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # 创建应用
    app = create_app()
    
    # 获取配置
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"""
    ╔══════════════════════════════════════╗
    ║          Cash Admin 启动中...         ║
    ╠══════════════════════════════════════╣
    ║  地址: http://{host}:{port}          ║
    ║  环境: {'开发' if debug else '生产'}模式              ║
    ║  调试: {'开启' if debug else '关闭'}                ║
    ╚══════════════════════════════════════╝
    """)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\n程序已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
