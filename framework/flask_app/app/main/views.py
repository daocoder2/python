from flask import render_template, redirect, request, url_for, flash
from . import main
from datetime import datetime


@main.route('/redirect')
def redirect_url():
    # abort(500)
    url = url_for('index', test='test', _external=True)
    return redirect(url, 302)


@main.route('/template')
def template():
    comments = {'test': 'test', 'test1': 'test1',  'test2': 'test2'}
    return render_template('template.html', comments=comments)


@main.route('/extends')
def extends():
    return render_template('extends.html', current_time=datetime.utcnow())


@main.route('/test')
def test():
    return render_template('main/test.html', current_time=datetime.utcnow())


# 错误定义页面这个参数e是必须的
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
