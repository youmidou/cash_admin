#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import struct
import json
import time

def debug_connection():
    """调试连接"""
    print("开始调试连接...")
    
    try:
        # 连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 1249))
        print("✅ 连接成功")
        
        # 准备登录请求 - 游戏服务器期望的格式是 [cmd, data]
        login_data = [
            'login',
            {
                'uuid': 'cash_admin_uuid',
                'device_id': 'cash_admin_device',
                'version': '1.0.0',
                'admin_key': 'admin_key_20250906'
            }
        ]
        
        json_data = json.dumps(login_data)
        print(f"发送数据: {json_data}")
        
        # 添加长度头
        length = len(json_data.encode('utf-8'))
        header = struct.pack('!I', length)
        print(f"数据长度: {length}, 头部: {header.hex()}")
        
        # 发送数据
        full_data = header + json_data.encode('utf-8')
        sock.send(full_data)
        print(f"已发送 {len(full_data)} 字节")
        
        # 接收响应头
        print("等待响应头...")
        response_header = sock.recv(4)
        print(f"响应头: {response_header.hex()}, 长度: {len(response_header)}")
        
        if len(response_header) == 4:
            response_length = struct.unpack('!I', response_header)[0]
            print(f"响应数据长度: {response_length}")
            
            # 接收响应数据
            response_data = b''
            while len(response_data) < response_length:
                chunk = sock.recv(response_length - len(response_data))
                if not chunk:
                    print("连接中断")
                    break
                response_data += chunk
                print(f"接收到 {len(chunk)} 字节，总共 {len(response_data)} 字节")
            
            if len(response_data) == response_length:
                try:
                    response_json = json.loads(response_data.decode('utf-8'))
                    print(f"✅ 响应成功: {response_json}")
                except Exception as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"原始数据: {response_data}")
            else:
                print(f"❌ 数据长度不匹配: 期望 {response_length}, 实际 {len(response_data)}")
        else:
            print(f"❌ 响应头长度错误: {len(response_header)}")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_connection()
