# Cash Admin - 游戏服务器管理后台

这是一个为 Cash Server 游戏服务器设计的 Web 管理后台系统，提供用户管理、主题管理、配置管理、活动管理等功能。

## 功能特性

### 🎮 用户管理
- 用户列表查看和搜索
- 用户详细信息查看
- 用户信息编辑（等级、VIP、金币等）
- 发送奖励给用户
- 用户作弊功能
- 删除用户账户

### 🎨 主题管理
- 主题列表查看
- 主题配置管理
- 主题状态控制
- 主题用户统计

### ⚙️ 配置管理
- 每日配置管理
- 活动配置管理
- AC（人工控制）配置
- 系统配置查看

### 📅 活动管理
- 活动列表查看
- 创建和编辑活动
- 活动参与者管理
- 活动状态控制

### 📊 仪表板
- 系统状态概览
- 用户统计信息
- 实时数据监控
- 快速操作入口

## 技术栈

- **后端**: Flask (Python)
- **前端**: Bootstrap 5 + jQuery
- **样式**: 自定义 CSS
- **图标**: Font Awesome
- **通信**: HTTP API

## 安装和运行

### 1. 环境要求
- Python 3.7+
- pip

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 文件为 `.env` 并修改配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
GAME_SERVER_URL=http://localhost:5000
GAME_SERVER_ADMIN_KEY=your-admin-key-here
```

### 4. 运行应用
```bash
python app.py
```

应用将在 `http://localhost:5001` 启动。

## 项目结构

```
cash_admin/
├── app/
│   ├── __init__.py          # Flask 应用工厂
│   ├── api_client.py        # 游戏服务器 API 客户端
│   ├── main/                # 主页面模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── user/                # 用户管理模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── theme/               # 主题管理模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── config/              # 配置管理模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── activity/            # 活动管理模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/           # HTML 模板
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── user/
│   │   ├── theme/
│   │   ├── config/
│   │   └── activity/
│   └── static/              # 静态文件
│       ├── css/
│       ├── js/
│       └── images/
├── config.py                # 配置文件
├── app.py                   # 应用入口
├── requirements.txt         # 依赖包
└── README.md               # 说明文档
```

## API 接口

### 用户管理 API
- `GET /user/` - 用户列表
- `GET /user/<user_id>` - 用户详情
- `GET /user/<user_id>/edit` - 编辑用户
- `POST /user/<user_id>/edit` - 更新用户
- `POST /user/<user_id>/delete` - 删除用户
- `GET /user/<user_id>/send-prize` - 发送奖励
- `POST /user/<user_id>/send-prize` - 执行发送奖励
- `GET /user/<user_id>/cheat` - 作弊功能
- `POST /user/<user_id>/cheat` - 执行作弊

### 主题管理 API
- `GET /theme/` - 主题列表
- `GET /theme/<theme_id>` - 主题详情
- `GET /theme/<theme_id>/config` - 主题配置
- `POST /theme/<theme_id>/config` - 更新主题配置
- `GET /theme/<theme_id>/users` - 主题用户统计

### 配置管理 API
- `GET /config/` - 配置管理主页
- `GET /config/daily` - 每日配置
- `POST /config/daily` - 更新每日配置
- `GET /config/activity` - 活动配置
- `POST /config/activity` - 更新活动配置
- `GET /config/ac` - AC配置
- `POST /config/ac` - 更新AC配置
- `GET /config/system` - 系统配置

### 活动管理 API
- `GET /activity/` - 活动列表
- `GET /activity/create` - 创建活动
- `POST /activity/create` - 执行创建活动
- `GET /activity/<activity_id>` - 活动详情
- `GET /activity/<activity_id>/edit` - 编辑活动
- `POST /activity/<activity_id>/edit` - 更新活动
- `GET /activity/<activity_id>/participants` - 活动参与者

## 配置说明

### 游戏服务器连接
确保游戏服务器正在运行并且可以通过配置的 URL 访问。管理后台通过 HTTP API 与游戏服务器通信。

### 安全配置
- 修改默认的 `SECRET_KEY`
- 配置正确的 `GAME_SERVER_ADMIN_KEY`
- 在生产环境中使用 HTTPS

## 开发说明

### 添加新功能
1. 在相应的模块目录下创建新的路由
2. 在 `api_client.py` 中添加对应的 API 调用方法
3. 创建相应的 HTML 模板
4. 更新导航菜单

### 自定义样式
修改 `app/static/css/admin.css` 文件来自定义样式。

### 添加新的 API 接口
在 `app/api_client.py` 中的 `GameServerAPI` 类中添加新的方法。

## 部署

### 使用 Gunicorn 部署
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### 使用 Docker 部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

如有问题，请通过以下方式联系：
- 创建 GitHub Issue
- 发送邮件到项目维护者
