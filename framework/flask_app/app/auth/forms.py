from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class Login(FlaskForm):
    us = StringField(label=u'用户名', validators=[DataRequired()])
    ps = PasswordField(label=u'密码', validators=[DataRequired(), EqualTo('ps2', 'err')])
    ps2 = PasswordField(label=u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'提交')




