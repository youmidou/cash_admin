import requests
import json
from flask import current_app

class GameServerAPI:
    def __init__(self):
        # 从配置中获取服务器设置
        if current_app:
            self.host = current_app.config.get('GAME_SERVER_HOST', 'localhost')
            self.port = current_app.config.get('GAME_SERVER_PORT', 5000)
            self.admin_key = current_app.config.get('GAME_SERVER_ADMIN_KEY', 'admin_key_20250906')
        else:
            # 默认配置
            self.host = 'localhost'
            self.port = 5000
            self.admin_key = 'admin_key_20250906'
        
        self.base_url = f"http://{self.host}:{self.port}"
        self.headers = {
            'X-Admin-Key': self.admin_key,
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method, endpoint, data=None):
        """发送HTTP请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            else:
                return {'error': f'不支持的HTTP方法: {method}'}
            
            # 检查响应状态
            if response.status_code == 401:
                return {'error': 'Unauthorized', 'message': 'Invalid admin key'}
            elif response.status_code != 200:
                return {'error': f'HTTP {response.status_code}', 'message': response.text}
            
            # 解析JSON响应
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON response', 'message': response.text}
                
        except requests.exceptions.ConnectionError:
            return {'error': 'Connection refused', 'message': '无法连接到游戏服务器'}
        except requests.exceptions.Timeout:
            return {'error': 'Request timeout', 'message': '请求超时'}
        except Exception as e:
            return {'error': f'Request failed: {str(e)}'}
    
    # 用户管理相关 API
    def get_users(self, page=1, limit=50, search=None):
        """获取用户列表"""
        params = {'page': page, 'limit': limit}
        if search:
            params['search'] = search
        
        endpoint = '/api/admin/users'
        if params:
            query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
            endpoint += f'?{query_string}'
        
        return self._make_request('GET', endpoint)
    
    def get_online_users(self, page=1, limit=15):
        """获取在线用户列表"""
        return self._make_request('GET', f'/api/admin/online-users?page={page}&limit={limit}')
    
    def get_user_info(self, user_id):
        """获取用户详细信息"""
        return self._make_request('GET', f'/api/admin/user/{user_id}')
    
    def get_system_info(self):
        """获取系统信息"""
        return self._make_request('GET', '/api/admin/system')
    
    def get_themes(self, page=1, limit=20):
        """获取主题列表"""
        return self._make_request('GET', f'/api/admin/themes?page={page}&limit={limit}')
    
    def get_theme_detail(self, theme_id):
        """获取主题详情"""
        return self._make_request('GET', f'/api/admin/theme/{theme_id}')
    
    def get_theme_config(self, theme_id):
        """获取主题配置"""
        return self._make_request('GET', f'/api/admin/theme/{theme_id}/config')
    
    def set_theme_config(self, theme_id, config_data):
        """设置主题配置"""
        return self._make_request('POST', f'/api/admin/theme/{theme_id}/config', data=config_data)
    
    def get_user_info(self, user_id):
        """获取用户详细信息"""
        return self._make_request('GET', f'/api/admin/user/{user_id}')
    
    def kick_user(self, user_id):
        """踢出用户"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/kick')
    
    def ban_user(self, user_id, duration=3600):
        """封禁用户"""
        data = {'duration': duration}
        return self._make_request('POST', f'/api/admin/user/{user_id}/ban', data)
    
    def unban_user(self, user_id):
        """解封用户"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/unban')
    
    def modify_user_coins(self, user_id, coins):
        """修改用户金币"""
        data = {'coins': coins}
        return self._make_request('POST', f'/api/admin/user/{user_id}/coins', data)
    
    def modify_user_level(self, user_id, level):
        """修改用户等级"""
        data = {'level': level}
        return self._make_request('POST', f'/api/admin/user/{user_id}/level', data)
    
    def send_broadcast(self, message):
        """发送广播消息"""
        data = {'message': message}
        return self._make_request('POST', '/api/admin/broadcast', data)
    
    def update_user(self, user_id, user_data):
        """更新用户信息"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/update', data=user_data)
    
    def delete_user(self, user_id, confirm=True):
        """删除用户账户"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/delete', data={'confirm': confirm})
    
    def set_user_admin(self, user_id, is_admin):
        """设置用户为管理员"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/set-admin', data={'is_admin': is_admin})
    
    def force_user_logout(self, user_id):
        """强制用户退出"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/force-logout')
    
    # ==================== 系统管理 ====================
    
    def update_system_config(self, config_data):
        """更新系统配置"""
        return self._make_request('POST', '/api/admin/system/update-config', data=config_data)
    
    def set_today_begin(self, begin_time):
        """设置今日开始时间"""
        return self._make_request('POST', '/api/admin/system/set-today-begin', data={'begin_time': begin_time})
    
    def reset_system_time(self, reset_type='all'):
        """重置系统时间"""
        return self._make_request('POST', '/api/admin/system/reset-time', data={'reset_type': reset_type})
    
    # ==================== 用户管理 ====================
    
    def get_user_server_info(self, user_id):
        """获取用户服务器信息"""
        return self._make_request('GET', f'/api/admin/user/{user_id}/server-info')
    
    def get_user_theme_info(self, user_id):
        """获取用户主题信息"""
        return self._make_request('GET', f'/api/admin/user/{user_id}/theme-info')
    
    def set_user_theme_info(self, user_id, theme_data):
        """设置用户主题信息"""
        return self._make_request('POST', f'/api/admin/user/{user_id}/theme-info', data=theme_data)
    
    def get_user_map(self):
        """获取用户映射信息"""
        return self._make_request('GET', '/api/admin/user-map')
    
    # ==================== 主题管理 ====================
    
    def get_theme_users(self, theme_id):
        """获取主题用户信息"""
        return self._make_request('GET', f'/api/admin/theme/{theme_id}/users')
    
    def get_theme_config(self, theme_id):
        """获取主题配置"""
        return self._make_request('GET', f'/api/admin/theme/{theme_id}/config')
    
    def set_theme_config(self, theme_id, config_data):
        """设置主题配置"""
        return self._make_request('POST', f'/api/admin/theme/{theme_id}/config', data=config_data)
    
    # ==================== 奖励管理 ====================
    
    def send_prize(self, user_id, prize_type, amount, reason='管理员奖励'):
        """发送奖励给用户"""
        data = {
            'user_id': user_id,
            'prize_type': prize_type,
            'amount': amount,
            'reason': reason
        }
        return self._make_request('POST', '/api/admin/reward/send-prize', data=data)
    
    def add_inbox(self, user_id, item_type, item_id=None, quantity=1, title='管理员礼物', description=''):
        """添加收件箱物品"""
        data = {
            'user_id': user_id,
            'item_type': item_type,
            'item_id': item_id,
            'quantity': quantity,
            'title': title,
            'description': description
        }
        return self._make_request('POST', '/api/admin/reward/add-inbox', data=data)
    
    def delete_inbox_gift(self, user_id, gift_id):
        """删除收件箱礼物"""
        data = {
            'user_id': user_id,
            'gift_id': gift_id
        }
        return self._make_request('POST', '/api/admin/reward/delete-inbox-gift', data=data)
    
    def send_inbox_gift(self, user_id, gift_type, gift_data=None, sender_name='管理员', message=''):
        """发送收件箱礼物"""
        data = {
            'user_id': user_id,
            'gift_type': gift_type,
            'gift_data': gift_data or {},
            'sender_name': sender_name,
            'message': message
        }
        return self._make_request('POST', '/api/admin/reward/send-inbox-gift', data=data)
    
    # ==================== 作弊管理 ====================
    
    def execute_cheat(self, user_id, cheat_type, cheat_params=None, reason='管理员调试'):
        """执行作弊操作（调试用）"""
        data = {
            'user_id': user_id,
            'cheat_type': cheat_type,
            'cheat_params': cheat_params or {},
            'reason': reason
        }
        return self._make_request('POST', '/api/admin/cheat/execute', data=data)
    
    def respin_cheat(self, user_id, theme_id=10050, bet_amount=1000, target_result=None, reason='管理员调试'):
        """重新旋转作弊"""
        data = {
            'user_id': user_id,
            'theme_id': theme_id,
            'bet_amount': bet_amount,
            'target_result': target_result or {},
            'reason': reason
        }
        return self._make_request('POST', '/api/admin/cheat/respin', data=data)
    
    def clean_disconnect_data(self, user_id=None, clean_type='all', reason='管理员清理'):
        """清理断开连接数据"""
        data = {
            'user_id': user_id,
            'clean_type': clean_type,
            'reason': reason
        }
        return self._make_request('POST', '/api/admin/cheat/clean-disconnect-data', data=data)
    
    # ==================== 奖池管理 ====================
    
    def get_jackpot_info(self, theme_id):
        """获取指定主题的奖池信息"""
        return self._make_request('GET', f'/api/admin/jackpot/{theme_id}')
    
    def get_all_jackpot_info(self):
        """获取所有奖池信息"""
        return self._make_request('GET', '/api/admin/jackpot/all')
    
    def calculate_store_data(self, theme_id=None, calculation_type='all', date_range='today'):
        """计算商店数据"""
        data = {
            'theme_id': theme_id,
            'calculation_type': calculation_type,
            'date_range': date_range
        }
        return self._make_request('POST', '/api/admin/jackpot/calculate-store', data=data)
    
    # ==================== 报表管理 ====================
    
    def get_report_data(self, report_type='overview', date_range='today', theme_id=None, user_id=None, format_type='json'):
        """获取报表数据"""
        params = {
            'type': report_type,
            'date_range': date_range,
            'format': format_type
        }
        if theme_id:
            params['theme_id'] = theme_id
        if user_id:
            params['user_id'] = user_id
        
        return self._make_request('GET', '/api/admin/report', params=params)
    
    # ==================== 配置管理 ====================
    
    def get_daily_config(self):
        """获取每日配置"""
        return self._make_request('GET', '/api/admin/config/daily')
    
    def set_daily_config(self, config_data):
        """设置每日配置"""
        return self._make_request('POST', '/api/admin/config/daily', data=config_data)
    
    def get_update_config(self):
        """获取更新配置"""
        return self._make_request('GET', '/api/admin/config/update')
    
    def get_update_default_config(self):
        """获取更新默认配置"""
        return self._make_request('GET', '/api/admin/config/update/default')
    
    def set_update_config(self, config_data):
        """设置更新配置"""
        return self._make_request('POST', '/api/admin/config/update', data=config_data)
    
    # ==================== 活动管理 ====================
    
    def get_activity_config(self):
        """获取活动配置"""
        return self._make_request('GET', '/api/admin/activity/config')
    
    def set_activity_config(self, config_data):
        """设置活动配置"""
        return self._make_request('POST', '/api/admin/activity/config', data=config_data)
    
    def get_activity_default_config(self):
        """获取活动默认配置"""
        return self._make_request('GET', '/api/admin/activity/config/default')
    
    def get_ac_config(self):
        """获取AC配置"""
        return self._make_request('GET', '/api/admin/activity/ac/config')
    
    def set_ac_config(self, config_data):
        """设置AC配置"""
        return self._make_request('POST', '/api/admin/activity/ac/config', data=config_data)
    
    def get_ac_default_config(self):
        """获取AC默认配置"""
        return self._make_request('GET', '/api/admin/activity/ac/config/default')
    
    # ==================== 广播管理 ====================
    
    def get_broadcast_config(self):
        """获取广播配置"""
        return self._make_request('GET', '/api/admin/broadcast/config')
    
    def set_broadcast_config(self, config_data):
        """设置广播配置"""
        return self._make_request('POST', '/api/admin/broadcast/config', data=config_data)
    
    def get_broadcast_sender_key(self):
        """获取广播发送者密钥"""
        return self._make_request('GET', '/api/admin/broadcast/sender-key')
    
    def send_broadcast(self, broadcast_data):
        """发送广播消息"""
        return self._make_request('POST', '/api/admin/broadcast/send', data=broadcast_data)
    
    def get_broadcast_history(self, page=1, limit=20):
        """获取广播历史记录"""
        return self._make_request('GET', f'/api/admin/broadcast/history?page={page}&limit={limit}')
    
    def health_check(self):
        """健康检查"""
        return self._make_request('GET', '/health')
    
    # 兼容性方法 - 保持与原有代码的兼容性
    def get_user_map(self):
        """获取用户映射信息 - 兼容性方法"""
        return self.get_users()
    
    def update_user(self, user_id, updates):
        """更新用户信息 - 兼容性方法"""
        # 这里可以根据updates的内容调用不同的方法
        if 'coins' in updates:
            return self.modify_user_coins(user_id, updates['coins'])
        elif 'level' in updates:
            return self.modify_user_level(user_id, updates['level'])
        else:
            return {'error': 'Unsupported update operation'}
    
    def delete_account(self, user_id):
        """删除用户账户 - 兼容性方法"""
        # 这里可以实现删除逻辑，或者返回错误
        return {'error': 'Delete account not implemented'}
    
    def send_prize(self, user_id, prize_data):
        """发送奖励给用户 - 兼容性方法"""
        # 这里可以实现奖励发送逻辑
        return {'error': 'Send prize not implemented'}
    
    # 主题管理相关 API - 兼容性方法（已在上方实现）
    
    # 配置管理相关 API - 兼容性方法
    def get_daily_config(self):
        """获取每日配置 - 兼容性方法"""
        return {'error': 'Daily config API not implemented'}
    
    def set_daily_config(self, config):
        """设置每日配置 - 兼容性方法"""
        return {'error': 'Set daily config API not implemented'}
    
    def get_activity_config(self):
        """获取活动配置 - 兼容性方法"""
        return {'error': 'Activity config API not implemented'}
    
    def set_activity_config(self, config):
        """设置活动配置 - 兼容性方法"""
        return {'error': 'Set activity config API not implemented'}
    
    def get_ac_config(self):
        """获取 AC 配置 - 兼容性方法"""
        return {'error': 'AC config API not implemented'}
    
    def set_ac_config(self, config):
        """设置 AC 配置 - 兼容性方法"""
        return {'error': 'Set AC config API not implemented'}