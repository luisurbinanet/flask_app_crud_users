from flask_wtf import FlaskForm
from wtforms import StringField, FileField, ColorField, validators

def generate_settings_form(settings):
    class SettingsForm(FlaskForm):
        pass

    for setting in settings:
        if setting.key == 'logo':
            field = FileField(setting.label, validators=[validators.Optional()])
        elif 'color' in setting.key:
            field = ColorField(setting.label, validators=[validators.DataRequired()])
        else:
            field = StringField(setting.label, validators=[validators.DataRequired()])
        setattr(SettingsForm, setting.key, field)

    return SettingsForm
