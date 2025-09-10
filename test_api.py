#!/usr/bin/env python3
"""
测试cash_admin API的脚本
"""
import requests
import json

# 测试游戏服务器API
def test_game_server_api():
    print("=== 测试游戏服务器API ===")
    
    headers = {
        'X-Admin-Key': 'admin_key_20250906',
        'Content-Type': 'application/json'
    }
    
    # 测试健康检查
    try:
        response = requests.get('http://localhost:5001/health', headers=headers)
        print(f"健康检查: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"健康检查失败: {e}")
    
    # 测试系统信息
    try:
        response = requests.get('http://localhost:5001/api/admin/system', headers=headers)
        print(f"系统信息: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"系统信息失败: {e}")
    
    # 测试在线用户
    try:
        response = requests.get('http://localhost:5001/api/admin/online-users', headers=headers)
        print(f"在线用户: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"在线用户失败: {e}")

# 测试cash_admin API（需要登录）
def test_cash_admin_api():
    print("\n=== 测试cash_admin API ===")
    
    session = requests.Session()
    
    # 尝试访问登录页面
    try:
        response = session.get('http://localhost:5002/auth/login')
        print(f"登录页面: {response.status_code}")
    except Exception as e:
        print(f"登录页面失败: {e}")
    
    # 尝试登录（使用默认管理员账号）
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = session.post('http://localhost:5002/auth/login', data=login_data)
        print(f"登录尝试: {response.status_code}")
        
        # 如果登录成功，测试API
        if response.status_code == 302 or 'dashboard' in response.url:
            print("登录成功，测试API...")
            
            # 测试统计数据API
            try:
                response = session.get('http://localhost:5002/api/stats')
                print(f"统计数据: {response.status_code} - {response.json()}")
            except Exception as e:
                print(f"统计数据失败: {e}")
            
            # 测试在线用户API
            try:
                response = session.get('http://localhost:5002/user/api/online-users')
                print(f"在线用户API: {response.status_code} - {response.json()}")
            except Exception as e:
                print(f"在线用户API失败: {e}")
        else:
            print("登录失败")
            
    except Exception as e:
        print(f"登录失败: {e}")

if __name__ == '__main__':
    test_game_server_api()
    test_cash_admin_api()
