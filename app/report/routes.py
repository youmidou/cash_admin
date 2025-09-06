from flask import render_template, request, jsonify, flash, redirect, url_for
from app.report import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def report_management():
    """报表管理主页面"""
    return render_template('report/management.html')

@bp.route('/overview')
@login_required
def overview_report():
    """概览报表"""
    api = GameServerAPI()
    try:
        date_range = request.args.get('date_range', 'today')
        result = api.get_report_data('overview', date_range)
        
        if result.get('success'):
            report_data = result.get('data', {})
            return render_template('report/overview.html', 
                                 report_data=report_data,
                                 date_range=date_range)
        else:
            flash(f'获取概览报表失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('report.report_management'))
    except Exception as e:
        flash(f'获取概览报表失败: {str(e)}', 'error')
        return redirect(url_for('report.report_management'))

@bp.route('/user')
@login_required
def user_report():
    """用户报表"""
    api = GameServerAPI()
    try:
        date_range = request.args.get('date_range', 'today')
        result = api.get_report_data('user', date_range)
        
        if result.get('success'):
            report_data = result.get('data', {})
            return render_template('report/user.html', 
                                 report_data=report_data,
                                 date_range=date_range)
        else:
            flash(f'获取用户报表失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('report.report_management'))
    except Exception as e:
        flash(f'获取用户报表失败: {str(e)}', 'error')
        return redirect(url_for('report.report_management'))

@bp.route('/theme')
@login_required
def theme_report():
    """主题报表"""
    api = GameServerAPI()
    try:
        date_range = request.args.get('date_range', 'today')
        theme_id = request.args.get('theme_id')
        result = api.get_report_data('theme', date_range, theme_id)
        
        if result.get('success'):
            report_data = result.get('data', {})
            return render_template('report/theme.html', 
                                 report_data=report_data,
                                 date_range=date_range,
                                 theme_id=theme_id)
        else:
            flash(f'获取主题报表失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('report.report_management'))
    except Exception as e:
        flash(f'获取主题报表失败: {str(e)}', 'error')
        return redirect(url_for('report.report_management'))

@bp.route('/revenue')
@login_required
def revenue_report():
    """营收报表"""
    api = GameServerAPI()
    try:
        date_range = request.args.get('date_range', 'today')
        result = api.get_report_data('revenue', date_range)
        
        if result.get('success'):
            report_data = result.get('data', {})
            return render_template('report/revenue.html', 
                                 report_data=report_data,
                                 date_range=date_range)
        else:
            flash(f'获取营收报表失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('report.report_management'))
    except Exception as e:
        flash(f'获取营收报表失败: {str(e)}', 'error')
        return redirect(url_for('report.report_management'))

@bp.route('/activity')
@login_required
def activity_report():
    """活动报表"""
    api = GameServerAPI()
    try:
        date_range = request.args.get('date_range', 'today')
        result = api.get_report_data('activity', date_range)
        
        if result.get('success'):
            report_data = result.get('data', {})
            return render_template('report/activity.html', 
                                 report_data=report_data,
                                 date_range=date_range)
        else:
            flash(f'获取活动报表失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('report.report_management'))
    except Exception as e:
        flash(f'获取活动报表失败: {str(e)}', 'error')
        return redirect(url_for('report.report_management'))
