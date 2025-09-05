#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import base64
import hashlib
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad as pkcs5pad

# 添加游戏服务器路径到 Python 路径
sys.path.insert(0, '/Users/yh/Documents/github/cash_server')

# 切换到游戏服务器目录
os.chdir('/Users/yh/Documents/github/cash_server')

from models.initialize import Database
from models.user import User
from sys_module.property import Property
from models.user_persona import UserPersona
from models.user_info import UserInfo
import datetime

def prepare(key, iv, mode):
    """准备 DES 加密器"""
    m = hashlib.md5()
    m.update(key.encode('utf-8'))
    k = m.hexdigest()
    return DES.new(k[:8].encode('utf-8'), DES.MODE_CBC, k[8:16].encode('utf-8'))

def encrypt(data):
    """加密数据"""
    des = prepare('papaya social 1.5', '\x00'*8, 1)
    if isinstance(data, str):
        data = data.encode('utf-8')
    secret = base64.b64encode(des.encrypt(pkcs5pad(data, 8)))
    return secret

def makeu(data):
    """处理加密数据"""
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

def create_admin_user():
    """创建默认管理员账户"""
    try:
        with Database.get_db_session() as db_session:
            # 检查是否已存在管理员账户
            existing_admin = db_session.query(User).filter(User.id == 1).first()
            
            if existing_admin:
                print("✅ 管理员账户已存在 (ID: 1)")
                # 确保管理员权限已设置
                property_data = Property.get_property(1)
                if property_data and property_data._is_admin != 1:
                    property_data._is_admin = 1
                    property_data.save()
                    print("✅ 已设置管理员权限")
                else:
                    print("✅ 管理员权限已设置")
                return existing_admin
            
            # 创建新的管理员账户
            admin_user = User(
                id=1,
                device_pass='admin123',
                uuid='admin-uuid-001',
                coins=1000000,  # 100万金币
                exp=0,
                level=1,
                vip_level=10,   # 最高VIP等级
                vip_points=0,
                first_login=datetime.datetime.now(),
                last_login=datetime.datetime.now(),
                purchase_count=0,
                total_purchase=0,
                max_purchase=0,
                max_weekly_purchase=0
            )
            
            db_session.add(admin_user)
            db_session.commit()
            
            # 创建用户属性
            property_data = Property(admin_user)
            property_data._is_admin = 1  # 设置管理员权限
            property_data._r_level = 1
            property_data._r_level_max = 3
            property_data._r_points = 0
            property_data._last_login_date = int(datetime.datetime.now().timestamp())
            property_data._today_level_up_count = 0
            property_data._last_bet = 1000
            property_data.save()
            
            # 创建用户画像
            persona = UserPersona(
                user_id=1,
                user_source='admin',
                device_model='Admin Device',
                platform_type='Admin',
                app_version='1.0.0',
                os_version='Admin OS',
                country='CN',
                language='zh-CN',
                timezone='Asia/Shanghai'
            )
            db_session.add(persona)
            
            # 创建用户信息
            user_info = UserInfo(
                user_id=1,
                nickname='管理员',
                avatar='admin_avatar',
                gender=1,
                age=25,
                city='Beijing',
                province='Beijing',
                country='China'
            )
            db_session.add(user_info)
            
            db_session.commit()
            
            print("✅ 成功创建管理员账户:")
            print(f"   - 用户ID: {admin_user.id}")
            print(f"   - 设备密码: {admin_user.device_pass}")
            print(f"   - 金币: {admin_user.coins:,}")
            print(f"   - VIP等级: {admin_user.vip_level}")
            print(f"   - 管理员权限: 已设置")
            
            return admin_user
            
    except Exception as e:
        print(f"❌ 创建管理员账户失败: {e}")
        return None

def generate_admin_credential():
    """生成管理员登录凭证"""
    try:
        credential_data = {'user_id': 1, 'device_pass': 'admin123'}
        credential_json = json.dumps(credential_data, ensure_ascii=False)
        credential_encrypted = encrypt(credential_json)
        credential_str = makeu(credential_encrypted)
        
        print("✅ 管理员登录凭证:")
        print(f"   - 用户ID: 1")
        print(f"   - 设备密码: admin123")
        print(f"   - 加密凭证: {credential_str}")
        
        return credential_str
        
    except Exception as e:
        print(f"❌ 生成登录凭证失败: {e}")
        return None

if __name__ == "__main__":
    print("🔧 创建默认管理员账户...")
    
    # 创建管理员账户
    admin_user = create_admin_user()
    
    if admin_user:
        # 生成登录凭证
        credential = generate_admin_credential()
        
        print("\n🎉 管理员账户创建完成！")
        print("现在可以使用以下信息登录游戏服务器:")
        print("   - 用户ID: 1")
        print("   - 设备密码: admin123")
        print("   - 管理员权限: 已启用")
    else:
        print("💥 管理员账户创建失败！")
