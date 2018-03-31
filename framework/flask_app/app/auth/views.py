from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import Login


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        name = form.us.data
        pswd = form.ps.data
        pswd2 = form.ps2.data
        print(name, pswd, pswd2)
        return redirect('index')
    else:
        if request.method == 'POST':
            flash(u'信息有误，请重新输入！')
    return render_template('auth/login.html', form=form)


@auth.route('/index')
def index():
    return render_template('index.html')


@auth.route('/redirect')
def redirect_url():
    # abort(500)
    url = url_for('index', test='test', _external=True)
    return redirect(url, 302)


@auth.route('/template')
def template():
    comments = {'test': 'test', 'test1': 'test1',  'test2': 'test2'}
    return render_template('template.html', comments=comments)


# 错误定义页面这个参数e是必须的
@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@auth.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
