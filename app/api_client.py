import requests
import json
from flask import current_app

class GameServerAPI:
    def __init__(self):
        self.base_url = current_app.config['GAME_SERVER_URL']
        self.admin_key = current_app.config['GAME_SERVER_ADMIN_KEY']
    
    def _make_request(self, command, data=None):
        """向游戏服务器发送请求"""
        url = f"{self.base_url}/admin"
        payload = {
            'command': command,
            'data': data or {}
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-Admin-Key': self.admin_key
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    # 用户管理相关 API
    def get_users(self, page=1, limit=50, search=None):
        """获取用户列表"""
        data = {
            'page': page,
            'limit': limit
        }
        if search:
            data['search'] = search
        return self._make_request('admin_get_users', data)
    
    def get_user_info(self, user_id):
        """获取用户详细信息"""
        return self._make_request('admin_get_user_server_info', {'user_id': user_id})
    
    def update_user(self, user_id, updates):
        """更新用户信息"""
        data = {'user_id': user_id, 'updates': updates}
        return self._make_request('admin_update_user', data)
    
    def delete_account(self, user_id):
        """删除用户账户"""
        return self._make_request('admin_delete_account', {'user_id': user_id})
    
    def send_prize(self, user_id, prize_data):
        """发送奖励给用户"""
        data = {'user_id': user_id, 'prize': prize_data}
        return self._make_request('admin_send_prize', data)
    
    # 主题管理相关 API
    def get_themes(self):
        """获取所有主题列表"""
        return self._make_request('admin_get_themes')
    
    def get_theme(self, theme_id):
        """获取特定主题信息"""
        return self._make_request('admin_get_theme', {'theme_id': theme_id})
    
    def get_theme_config(self, theme_id):
        """获取主题配置"""
        return self._make_request('admin_get_theme_config', {'theme_id': theme_id})
    
    def set_theme_config(self, theme_id, config):
        """设置主题配置"""
        data = {'theme_id': theme_id, 'config': config}
        return self._make_request('admin_set_theme_config', data)
    
    # 配置管理相关 API
    def get_daily_config(self):
        """获取每日配置"""
        return self._make_request('admin_get_daily_config')
    
    def set_daily_config(self, config):
        """设置每日配置"""
        return self._make_request('admin_set_daily_config', {'config': config})
    
    def get_activity_config(self):
        """获取活动配置"""
        return self._make_request('admin_get_activity_config')
    
    def set_activity_config(self, config):
        """设置活动配置"""
        return self._make_request('admin_set_activity_config', {'config': config})
    
    def get_ac_config(self):
        """获取 AC 配置"""
        return self._make_request('admin_get_ac_config')
    
    def set_ac_config(self, config):
        """设置 AC 配置"""
        return self._make_request('admin_set_ac_config', {'config': config})
    
    # 系统管理相关 API
    def get_system_info(self):
        """获取系统信息"""
        return self._make_request('admin_get_system')
    
    def get_report(self, report_type, date_range=None):
        """获取报告"""
        data = {'report_type': report_type}
        if date_range:
            data['date_range'] = date_range
        return self._make_request('admin_get_report', data)
    
    def clean_disconnect_data(self):
        """清理断开连接的数据"""
        return self._make_request('admin_clean_disconnect_data')
    
    # 邮箱管理相关 API
    def send_inbox_gift(self, user_id, gift_data):
        """发送邮箱礼物"""
        data = {'user_id': user_id, 'gift': gift_data}
        return self._make_request('admin_send_inbox_gift', data)
    
    def delete_inbox_gift(self, gift_id):
        """删除邮箱礼物"""
        return self._make_request('admin_delete_inbox_gift', {'gift_id': gift_id})
    
    # 作弊功能相关 API
    def cheat(self, user_id, cheat_type, value):
        """执行作弊操作"""
        data = {
            'user_id': user_id,
            'cheat_type': cheat_type,
            'value': value
        }
        return self._make_request('admin_cheat', data)
    
    def respin_cheat(self, user_id, theme_id, respin_data):
        """执行重转作弊"""
        data = {
            'user_id': user_id,
            'theme_id': theme_id,
            'respin_data': respin_data
        }
        return self._make_request('admin_respin_cheat', data)
