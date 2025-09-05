import socket
import struct
import json
import time
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64
import hashlib
from flask import current_app

class GameServerAPI:
    def __init__(self):
        # 从配置中获取服务器设置
        if current_app:
            self.host = current_app.config.get('GAME_SERVER_HOST', 'localhost')
            self.port = current_app.config.get('GAME_SERVER_PORT', 1249)
            self.admin_key = current_app.config.get('GAME_SERVER_ADMIN_KEY', 'cash_admin_2024_secret_key')
        else:
            # 默认配置
            self.host = 'localhost'
            self.port = 1249
            self.admin_key = 'cash_admin_2024_secret_key'
        
        self.socket = None
        self.connected = False
        
    def _connect(self):
        """连接到游戏服务器"""
        try:
            if self.socket:
                self.socket.close()
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            self.connected = False
            return False
    
    def _disconnect(self):
        """断开连接"""
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False
    
    def _encrypt(self, data):
        """加密数据"""
        try:
            # 使用与游戏服务器相同的加密方式
            key = hashlib.md5('cash_admin_2024_secret_key'.encode('utf-8')).digest()[:8]
            iv = hashlib.md5('cash_admin_2024_secret_key'.encode('utf-8')).digest()[:8]
            
            cipher = DES.new(key, DES.MODE_CBC, iv)
            padded_data = pad(data.encode('utf-8'), 8)
            encrypted = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            print(f"加密失败: {e}")
            return None
    
    def _makeu(self, encrypted_data):
        """生成 makeu 格式的数据"""
        try:
            # 简单的 makeu 实现
            return encrypted_data
        except Exception as e:
            print(f"makeu 失败: {e}")
            return None
    
    def _send_request(self, command, data=None):
        """发送请求到游戏服务器"""
        try:
            if not self.connected:
                if not self._connect():
                    return {'error': '无法连接到游戏服务器'}
            
            # 准备请求数据
            request_data = {
                'cmd': command
            }
            if data:
                request_data.update(data)
            
            # 转换为 JSON
            json_data = json.dumps(request_data)
            
            # 添加长度头 (使用网络字节序，与游戏服务器一致)
            length = len(json_data.encode('utf-8'))
            header = struct.pack('!I', length)
            
            # 发送数据
            self.socket.send(header + json_data.encode('utf-8'))
            
            # 接收响应
            response_header = self.socket.recv(4)
            if len(response_header) != 4:
                return {'error': '响应头长度错误'}
            
            response_length = struct.unpack('!I', response_header)[0]
            response_data = b''
            
            while len(response_data) < response_length:
                chunk = self.socket.recv(response_length - len(response_data))
                if not chunk:
                    return {'error': '连接中断'}
                response_data += chunk
            
            # 解析响应
            response_json = json.loads(response_data.decode('utf-8'))
            return response_json
            
        except Exception as e:
            print(f"发送请求失败: {e}")
            self.connected = False
            return {'error': f'请求失败: {str(e)}'}
    
    def _login_admin(self):
        """以管理员身份登录"""
        try:
            # 发送登录请求，使用 admin_key 参数
            login_data = {
                'uuid': 'cash_admin_uuid',
                'device_id': 'cash_admin_device',
                'version': '1.0.0',
                'admin_key': 'admin_key_20250906'  # 使用游戏服务器中定义的管理员密钥
            }
            
            response = self._send_request('CMD_LOGIN', login_data)
            if response.get('success') or 'credential' in response:
                print("管理员登录成功")
                return True
            else:
                print(f"管理员登录失败: {response}")
                return False
                
        except Exception as e:
            print(f"管理员登录异常: {e}")
            return False
    
    def _ensure_admin_login(self):
        """确保已以管理员身份登录"""
        if not self.connected:
            if not self._connect():
                return False
        
        # 尝试登录管理员
        return self._login_admin()
    
    # 用户管理相关 API
    def get_users(self, page=1, limit=50, search=None):
        """获取用户列表"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        data = {'page': page, 'limit': limit}
        if search:
            data['search'] = search
        
        return self._send_request('CMD_ADMIN_GET_USERS', data)
    
    def get_online_users(self):
        """获取在线用户数量"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_INDEX_GET_PERSON_NUM')
    
    def get_user_map(self):
        """获取用户映射信息"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_USER_MAP')
    
    def get_system_info(self):
        """获取系统信息（包含在线用户）"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_SYSTEM')
    
    def get_user_info(self, user_id):
        """获取用户详细信息"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_USERS', {'uid': user_id})
    
    def update_user(self, user_id, updates):
        """更新用户信息"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        data = {'uid': user_id, 'updates': updates}
        return self._send_request('CMD_ADMIN_GET_USERS', data)
    
    def delete_account(self, user_id):
        """删除用户账户"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_USERS', {'uid': user_id, 'action': 'delete'})
    
    def send_prize(self, user_id, prize_data):
        """发送奖励给用户"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        data = {'uid': user_id, 'prize': prize_data}
        return self._send_request('CMD_ADMIN_SEND_PRIZE', data)
    
    # 主题管理相关 API
    def get_themes(self):
        """获取所有主题列表"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_THEMES')
    
    def get_theme(self, theme_id):
        """获取特定主题信息"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_THEME', {'tid': theme_id})
    
    def get_theme_config(self, theme_id):
        """获取主题配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_THEME_CONFIG', {'tid': theme_id})
    
    def set_theme_config(self, theme_id, config):
        """设置主题配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        data = {'tid': theme_id, 'config': config}
        return self._send_request('CMD_ADMIN_SET_THEME_CONFIG', data)
    
    # 配置管理相关 API
    def get_daily_config(self):
        """获取每日配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_DAILY_CONFIG')
    
    def set_daily_config(self, config):
        """设置每日配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_SET_DAILY_CONFIG', {'config': config})
    
    def get_activity_config(self):
        """获取活动配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_ACTIVITY_CONFIG')
    
    def set_activity_config(self, config):
        """设置活动配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_SET_ACTIVITY_CONFIG', {'config': config})
    
    def get_ac_config(self):
        """获取 AC 配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_GET_AC_CONFIG')
    
    def set_ac_config(self, config):
        """设置 AC 配置"""
        if not self._ensure_admin_login():
            return {'error': '管理员登录失败'}
        
        return self._send_request('CMD_ADMIN_SET_AC_CONFIG', {'config': config})
    
    def __del__(self):
        """析构函数，确保连接被关闭"""
        self._disconnect()