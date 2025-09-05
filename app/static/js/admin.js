// 全局 JavaScript 功能

$(document).ready(function() {
    // 初始化工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 自动隐藏警告消息
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // 确认删除对话框
    $('.btn-delete').click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        if (confirm('确定要删除吗？此操作不可撤销！')) {
            window.location.href = url;
        }
    });

    // 数字格式化
    $('.number-format').each(function() {
        var num = parseInt($(this).text());
        if (!isNaN(num)) {
            $(this).text(num.toLocaleString());
        }
    });

    // 时间格式化
    $('.time-format').each(function() {
        var time = $(this).text();
        if (time && time !== 'N/A') {
            var date = new Date(time);
            $(this).text(date.toLocaleString('zh-CN'));
        }
    });
});

// 工具函数
const AdminUtils = {
    // 格式化数字
    formatNumber: function(num) {
        return num.toLocaleString();
    },

    // 格式化时间
    formatTime: function(time) {
        if (!time || time === 'N/A') return 'N/A';
        return new Date(time).toLocaleString('zh-CN');
    },

    // 显示加载状态
    showLoading: function(element) {
        $(element).html('<i class="fas fa-spinner fa-spin"></i> 加载中...');
    },

    // 隐藏加载状态
    hideLoading: function(element, originalText) {
        $(element).text(originalText);
    },

    // 显示成功消息
    showSuccess: function(message) {
        this.showAlert(message, 'success');
    },

    // 显示错误消息
    showError: function(message) {
        this.showAlert(message, 'danger');
    },

    // 显示警告消息
    showWarning: function(message) {
        this.showAlert(message, 'warning');
    },

    // 显示信息消息
    showInfo: function(message) {
        this.showAlert(message, 'info');
    },

    // 显示警告框
    showAlert: function(message, type) {
        var alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        $('.container-fluid').prepend(alertHtml);
        
        // 自动隐藏
        setTimeout(function() {
            $('.alert').fadeOut('slow');
        }, 5000);
    },

    // 确认对话框
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // AJAX 请求封装
    ajax: function(url, data, method = 'POST') {
        return $.ajax({
            url: url,
            method: method,
            data: data,
            dataType: 'json',
            beforeSend: function() {
                // 显示加载状态
            },
            complete: function() {
                // 隐藏加载状态
            }
        });
    },

    // 复制到剪贴板
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(function() {
            AdminUtils.showSuccess('已复制到剪贴板');
        }).catch(function() {
            AdminUtils.showError('复制失败');
        });
    },

    // 下载文件
    downloadFile: function(url, filename) {
        var link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};

// 用户管理相关功能
const UserManager = {
    // 搜索用户
    searchUser: function(query) {
        if (query.length < 2) return;
        
        $.get('/api/users/search', { q: query })
            .done(function(data) {
                // 处理搜索结果
            })
            .fail(function() {
                AdminUtils.showError('搜索失败');
            });
    },

    // 批量操作
    batchOperation: function(operation, userIds) {
        if (userIds.length === 0) {
            AdminUtils.showWarning('请选择要操作的用户');
            return;
        }

        AdminUtils.confirm(`确定要${operation}选中的${userIds.length}个用户吗？`, function() {
            $.post('/api/users/batch', {
                operation: operation,
                user_ids: userIds
            }).done(function(data) {
                AdminUtils.showSuccess('批量操作完成');
                location.reload();
            }).fail(function() {
                AdminUtils.showError('批量操作失败');
            });
        });
    }
};

// 主题管理相关功能
const ThemeManager = {
    // 切换主题状态
    toggleThemeStatus: function(themeId, status) {
        $.post('/api/themes/toggle', {
            theme_id: themeId,
            status: status
        }).done(function(data) {
            AdminUtils.showSuccess('主题状态更新成功');
            location.reload();
        }).fail(function() {
            AdminUtils.showError('主题状态更新失败');
        });
    },

    // 重置主题配置
    resetThemeConfig: function(themeId) {
        AdminUtils.confirm('确定要重置主题配置吗？', function() {
            $.post('/api/themes/reset', {
                theme_id: themeId
            }).done(function(data) {
                AdminUtils.showSuccess('主题配置重置成功');
                location.reload();
            }).fail(function() {
                AdminUtils.showError('主题配置重置失败');
            });
        });
    }
};

// 配置管理相关功能
const ConfigManager = {
    // 保存配置
    saveConfig: function(configType, configData) {
        $.post('/api/config/save', {
            type: configType,
            data: configData
        }).done(function(data) {
            AdminUtils.showSuccess('配置保存成功');
        }).fail(function() {
            AdminUtils.showError('配置保存失败');
        });
    },

    // 重置配置
    resetConfig: function(configType) {
        AdminUtils.confirm('确定要重置配置吗？', function() {
            $.post('/api/config/reset', {
                type: configType
            }).done(function(data) {
                AdminUtils.showSuccess('配置重置成功');
                location.reload();
            }).fail(function() {
                AdminUtils.showError('配置重置失败');
            });
        });
    }
};

// 活动管理相关功能
const ActivityManager = {
    // 启动活动
    startActivity: function(activityId) {
        $.post('/api/activities/start', {
            activity_id: activityId
        }).done(function(data) {
            AdminUtils.showSuccess('活动启动成功');
            location.reload();
        }).fail(function() {
            AdminUtils.showError('活动启动失败');
        });
    },

    // 停止活动
    stopActivity: function(activityId) {
        AdminUtils.confirm('确定要停止这个活动吗？', function() {
            $.post('/api/activities/stop', {
                activity_id: activityId
            }).done(function(data) {
                AdminUtils.showSuccess('活动停止成功');
                location.reload();
            }).fail(function() {
                AdminUtils.showError('活动停止失败');
            });
        });
    }
};

// 导出全局对象
window.AdminUtils = AdminUtils;
window.UserManager = UserManager;
window.ThemeManager = ThemeManager;
window.ConfigManager = ConfigManager;
window.ActivityManager = ActivityManager;
