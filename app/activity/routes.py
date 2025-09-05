from flask import render_template, request, jsonify, flash, redirect, url_for
from app.activity import bp
from app.api_client import GameServerAPI

@bp.route('/')
def activity_list():
    """活动列表页面"""
    api = GameServerAPI()
    activities_data = api.get_activity_config()
    
    return render_template('activity/list.html', activities_data=activities_data)

@bp.route('/create', methods=['GET', 'POST'])
def create_activity():
    """创建活动"""
    if request.method == 'POST':
        activity_data = {
            'name': request.form.get('name'),
            'type': request.form.get('type'),
            'start_time': request.form.get('start_time'),
            'end_time': request.form.get('end_time'),
            'description': request.form.get('description'),
            'rewards': request.form.get('rewards'),
            'conditions': request.form.get('conditions')
        }
        
        # 这里可以添加创建活动的API调用
        flash('活动创建成功', 'success')
        return redirect(url_for('activity.activity_list'))
    
    return render_template('activity/create.html')

@bp.route('/<int:activity_id>')
def activity_detail(activity_id):
    """活动详情页面"""
    # 这里可以添加获取活动详情的API调用
    activity_info = {
        'id': activity_id,
        'name': '示例活动',
        'type': 'daily',
        'status': 'active',
        'participants': 1250,
        'total_rewards': 50000
    }
    
    return render_template('activity/detail.html', activity_info=activity_info)

@bp.route('/<int:activity_id>/edit', methods=['GET', 'POST'])
def edit_activity(activity_id):
    """编辑活动"""
    if request.method == 'POST':
        # 这里可以添加更新活动的API调用
        flash('活动更新成功', 'success')
        return redirect(url_for('activity.activity_detail', activity_id=activity_id))
    
    # 获取活动信息
    activity_info = {
        'id': activity_id,
        'name': '示例活动',
        'type': 'daily',
        'start_time': '2024-01-01T00:00:00',
        'end_time': '2024-01-31T23:59:59',
        'description': '这是一个示例活动',
        'rewards': '{"coins": 1000, "gems": 100}',
        'conditions': '{"level": 5}'
    }
    
    return render_template('activity/edit.html', activity_info=activity_info)

@bp.route('/<int:activity_id>/participants')
def activity_participants(activity_id):
    """活动参与者页面"""
    # 这里可以添加获取活动参与者的API调用
    participants_data = {
        'participants': [
            {'id': 1, 'name': '用户1', 'score': 1000, 'rank': 1},
            {'id': 2, 'name': '用户2', 'score': 950, 'rank': 2},
            {'id': 3, 'name': '用户3', 'score': 900, 'rank': 3}
        ],
        'total': 3
    }
    
    return render_template('activity/participants.html', 
                         activity_id=activity_id, 
                         participants_data=participants_data)
