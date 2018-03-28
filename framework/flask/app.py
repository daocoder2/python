#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, \
    abort, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
# mysql://username:passwd@localhost/mydatabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True


# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint, url_prefix='/auth')

username = ''


@app.before_request
def before_request():
    global username
    username = 'daocoder'


@app.route('/index')
def index():
    print(app.url_map)
    user_agent = request.headers.get('User-Agent')
    response = make_response('<p>Your browser is %s</p>' % user_agent)
    return response, 400


@app.route('/redirect')
def redirect_url():
    # abort(500)
    url = url_for('index', test='test', _external=True)
    return redirect(url, 302)


@app.route('/template')
def template():
    comments = {'test': 'test', 'test1': 'test1',  'test2': 'test2'}
    return render_template('template.html', comments=comments)


@app.route('/extends')
def extends():
    return render_template('extends.html')


# 错误定义页面这个参数e是必须的
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
