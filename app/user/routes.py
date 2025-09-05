from flask import render_template, request, jsonify, flash, redirect, url_for
from app.user import bp
from app.api_client import GameServerAPI
from app.auth import login_required
import time

@bp.route('/')
@login_required
def user_list():
    """用户列表页面"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    api = GameServerAPI()
    
    # 获取在线用户数量
    online_data = api.get_online_users()
    online_count = online_data.get('online_user_num', 0) if online_data.get('error') is None else 0
    
    # 获取系统信息（包含在线用户列表）
    system_info = api.get_system_info()
    
    # 获取用户映射信息
    user_map_data = api.get_user_map()
    
    # 处理真实的游戏服务器数据
    users_data = {
        'users': [],
        'total': 0,
        'total_pages': 1,
        'online_count': online_count
    }
    
    # 从在线用户数据中获取用户信息
    if online_data.get('error') is None and online_data.get('data'):
        online_users = online_data.get('data', [])
        
        # 为每个在线用户创建详细信息
        for user in online_users:
            user_info = {
                'id': user.get('user_id', 'N/A'),
                'username': user.get('username', f'User_{user.get("user_id", "N/A")}'),
                'level': user.get('level', 1),
                'vip_level': user.get('vip_level', 0),  # 从用户数据获取VIP等级
                'coins': user.get('coins', 0),
                'gems': user.get('gems', 0),  # 从用户数据获取宝石
                'total_purchase': user.get('total_purchase', 0),  # 累积充值
                'register_time': user.get('register_time', 'N/A'),
                'last_login': user.get('login_time', 'N/A'),
                'is_online': True,  # 这些是从在线用户列表获取的
                'platform_type': user.get('platform_type', 'Unknown'),
                'device_model': 'Unknown'
            }
            users_data['users'].append(user_info)
        
        users_data['total'] = len(online_users)
        users_data['online_count'] = len(online_users)
        
        # 实现搜索功能
        if search:
            # 根据用户ID或用户名进行搜索
            filtered_users = []
            for user in users_data['users']:
                user_id_str = str(user['id'])
                username = user.get('username', '')
                if (search.lower() in user_id_str.lower() or 
                    search.lower() in username.lower()):
                    filtered_users.append(user)
            users_data['users'] = filtered_users
            users_data['total'] = len(filtered_users)
    else:
        # 如果无法获取系统信息，显示错误信息
        users_data = {
            'users': [],
            'total': 0,
            'total_pages': 1,
            'online_count': 0,
            'error': '无法连接到游戏服务器'
        }
    
    return render_template('user/list.html', 
                         users_data=users_data,
                         current_page=page,
                         search=search,
                         online_count=online_count)

@bp.route('/<int:user_id>')
@login_required
def user_detail(user_id):
    """用户详情页面"""
    api = GameServerAPI()
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/detail.html', user_info=user_info)

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    """编辑用户信息"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        updates = {}
        
        # 收集表单数据
        if request.form.get('level'):
            updates['level'] = int(request.form.get('level'))
        if request.form.get('vip_level'):
            updates['vip_level'] = int(request.form.get('vip_level'))
        if request.form.get('coins'):
            updates['coins'] = int(request.form.get('coins'))
        if request.form.get('gems'):
            updates['gems'] = int(request.form.get('gems'))
        
        result = api.update_user(user_id, updates)
        
        if result.get('error'):
            flash(f'更新用户失败: {result["error"]}', 'error')
        else:
            flash('用户信息更新成功', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    
    # GET 请求，获取用户信息
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/edit.html', user_info=user_info)

@bp.route('/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    """删除用户账户"""
    api = GameServerAPI()
    result = api.delete_account(user_id)
    
    if result.get('error'):
        flash(f'删除用户失败: {result["error"]}', 'error')
    else:
        flash('用户账户删除成功', 'success')
    
    return redirect(url_for('user.user_list'))

@bp.route('/<int:user_id>/send-prize', methods=['GET', 'POST'])
def send_prize(user_id):
    """发送奖励给用户"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        prize_data = {
            'type': request.form.get('prize_type'),
            'amount': int(request.form.get('amount', 0)),
            'message': request.form.get('message', '')
        }
        
        result = api.send_prize(user_id, prize_data)
        
        if result.get('error'):
            flash(f'发送奖励失败: {result["error"]}', 'error')
        else:
            flash('奖励发送成功', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    
    # GET 请求，获取用户信息
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/send_prize.html', user_info=user_info)

@bp.route('/<int:user_id>/cheat', methods=['GET', 'POST'])
def user_cheat(user_id):
    """用户作弊功能"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        cheat_type = request.form.get('cheat_type')
        value = request.form.get('value')
        
        result = api.cheat(user_id, cheat_type, value)
        
        if result.get('error'):
            flash(f'执行作弊失败: {result["error"]}', 'error')
        else:
            flash('作弊执行成功', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    
    # GET 请求，获取用户信息
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/cheat.html', user_info=user_info)

@bp.route('/api/online-users')
@login_required
def api_online_users():
    """获取在线用户数据的 API"""
    api = GameServerAPI()
    
    try:
        # 获取在线用户数据
        online_data = api.get_online_users()
        if online_data.get('error'):
            return jsonify({'error': online_data['error']}), 500
        
        # 获取在线用户列表和数量
        online_users = online_data.get('data', [])
        online_count = online_data.get('online_user_num', len(online_users))
        
        # 获取系统信息
        system_info = api.get_system_info()
        
        return jsonify({
            'online_count': online_count,
            'online_users': online_users,
            'system_info': system_info,
            'timestamp': int(time.time())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
