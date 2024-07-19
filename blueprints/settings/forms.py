from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

class SettingsForm(FlaskForm):
    app_name = StringField('Application Name', validators=[DataRequired()])
    logo = FileField('Logo')
    primary_color = StringField('Primary Color')
    secondary_color = StringField('Secondary Color')
    success_color = StringField('Success Color')
    warning_color = StringField('Warning Color')
    danger_color = StringField('Danger Color')
    error_color = StringField('Error Color')
