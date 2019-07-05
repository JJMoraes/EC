from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('', render_kw={"placeholder":"Username"}, validators=[
        DataRequired(), Length(1, 64)
    ])
    email = StringField('', render_kw={"placeholder":"E-mail"}, validators=[
        DataRequired()
    ])
    avatar = FileField('', render_kw={"placeholder":"Avatar"}, validators=[
        DataRequired()
    ])
    about_me = TextAreaField('', render_kw={"placeholder":"Sobre você"}, validators=[
        DataRequired()
    ])
    password = PasswordField('', render_kw={"placeholder":"Senha"}, validators=[
        DataRequired()
    ])
    password2 = PasswordField('', render_kw={"placeholder":"Confirmação de Senha"}, validators=[
        DataRequired(), EqualTo('password', message='Senhas não conferem.')
    ])
    submit = SubmitField('Registrar')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError("Usuário já registrado.")



class LoginForm(FlaskForm):
    username = StringField('', render_kw={"placeholder":"Username"}, validators=[
        DataRequired()
    ])
    password = PasswordField('', render_kw={"placeholder":"Password"}, validators=[
        DataRequired()
    ])
    submit = SubmitField('Enviar')
