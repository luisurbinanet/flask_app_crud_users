from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    avatar = FileField('Avatar')
    role_id = SelectField('Role', coerce=int)
