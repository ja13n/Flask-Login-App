from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField


class MyForm(FlaskForm):
    username = StringField("USERNAME", validators=[DataRequired()])
    password = PasswordField("PASSWORD", validators=[DataRequired()])
    remember = BooleanField("Remember Me")


class NewAccount(FlaskForm):
    username = StringField("USERNAME", validators=[DataRequired()])
    password = PasswordField("PASSWORD", validators=[DataRequired()])
    confirm_password = PasswordField("CONFIRM PASSWORD", validators=[DataRequired(), EqualTo("password")])