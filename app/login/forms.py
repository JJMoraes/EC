from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField, TextAreaField, FileField, \
    SelectMultipleField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo

from app.models import Role, User, Permission

class RoleForm(FlaskForm):
    name = StringField('', validators=[
        DataRequired()
    ])
    submit = SubmitField('Cadastrar')

    def validate_name(self, field):
        role = Role.query.filter_by(name=field.data).first()
        if role:
            raise ValidationError('FunÃ§Ã£o jÃ¡ cadastrada')


class EditProfileForm(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Username"}, validators=[
        DataRequired(), Length(1, 64)
    ])
    email = StringField('', render_kw={"placeholder": "E-mail"}, validators=[
        DataRequired()
    ])
    password = PasswordField('', render_kw={"placeholder": "Nova Senha"})
    password2 = PasswordField('', render_kw={"placeholder": "Confirmação de Nova Senha"}, validators=[EqualTo('password', message='Senhas não conferem.')
    ])
    submit = SubmitField('Enviar')


class EditProfileAdminForm(FlaskForm):
    role = SelectField('', coerce=int)
    status = SelectField('', choices=[('I','Inativo'), ('A', 'Ativo')])
    submit = SubmitField('Enviar')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name)
            for role in Role.query.all()
        ]
        self.user = user

class RoleForm(FlaskForm):
    name = StringField('', render_kw={"placeholder":"Nome"}, validators=[
        DataRequired()
    ])
    perms = [
        (str(Permission.FOLLOW), 'Follow'), (str(Permission.COMMENT), 'Comment'), (str(Permission.WRITE), 'Write'),
        (str(Permission.MODERATE), 'Moderate'), (str(Permission.ADMIN), 'Administrator')
    ]
    permissions = SelectMultipleField(choices=perms, default='1')
    submit = SubmitField('Cadastrar')

    def validate_name(self, field):
        role = Role.query.filter_by(name=field.data).first()
        if role:
            raise ValidationError('Função já cadastrada')

class ToPostForm(FlaskForm):
    title = StringField('', render_kw={"placeholder":"Title"}, validators=[DataRequired()])
    lide = TextAreaField('', render_kw={"placeholder":"Lide"}, validators=[DataRequired()])
    text = TextAreaField('', render_kw={"placeholder":"Texto"}, validators=[DataRequired()])
    image = FileField('', render_kw={"placeholder":"Imagem"}, validators=[DataRequired()])
    subtitle = StringField('', render_kw={"placeholder":"Legenda"}, validators=[DataRequired()])
    submit = SubmitField('Enviar')