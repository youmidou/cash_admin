#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api_client import GameServerAPI

def test_connection():
    """测试与游戏服务器的连接"""
    print("开始测试与游戏服务器的连接...")
    
    api = GameServerAPI()
    
    # 测试连接
    print("1. 测试连接...")
    if not api._connect():
        print("❌ 连接失败")
        return False
    print("✅ 连接成功")
    
    # 测试管理员登录
    print("2. 测试管理员登录...")
    if not api._login_admin():
        print("❌ 管理员登录失败")
        return False
    print("✅ 管理员登录成功")
    
    # 测试获取系统信息
    print("3. 测试获取系统信息...")
    system_info = api.get_system_info()
    if 'error' in system_info:
        print(f"❌ 获取系统信息失败: {system_info['error']}")
        return False
    print("✅ 获取系统信息成功")
    print(f"   系统信息: {system_info}")
    
    # 测试获取在线用户
    print("4. 测试获取在线用户...")
    online_users = api.get_online_users()
    if 'error' in online_users:
        print(f"❌ 获取在线用户失败: {online_users['error']}")
        return False
    print("✅ 获取在线用户成功")
    print(f"   在线用户: {online_users}")
    
    # 测试获取用户列表
    print("5. 测试获取用户列表...")
    users = api.get_users()
    if 'error' in users:
        print(f"❌ 获取用户列表失败: {users['error']}")
        return False
    print("✅ 获取用户列表成功")
    print(f"   用户列表: {users}")
    
    print("\n🎉 所有测试通过！cash_admin 可以正常连接游戏服务器")
    return True

if __name__ == '__main__':
    test_connection()