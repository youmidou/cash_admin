from flask import render_template, request, redirect, url_for, flash, session
from app.auth import bp
from app.auth import verify_admin_credentials, get_admin_info

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """管理员登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('请输入用户名和密码', 'error')
            return render_template('auth/login.html')
        
        if verify_admin_credentials(username, password):
            # 登录成功
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_info'] = get_admin_info(username)
            
            flash(f'欢迎回来，{username}！', 'success')
            
            # 重定向到之前访问的页面或仪表板
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """管理员登出"""
    session.clear()
    flash('已成功登出', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/profile')
def profile():
    """管理员个人资料页面"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    admin_info = session.get('admin_info', {})
    return render_template('auth/profile.html', admin_info=admin_info)
