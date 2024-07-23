from flask import render_template, redirect, url_for, flash, request
from . import settings_bp
from .forms import generate_settings_form
from extensions import db
from models import Settings

module = 'Configuración'

# Valores predeterminados
default_settings = [
    {'key': 'app_name', 'label': 'Nombre de la Aplicación', 'value': 'My Application'},
    {'key': 'logo', 'label': 'Logo', 'value': ''},
    {'key': 'primary_color', 'label': 'Color Primario', 'value': '#0000FF'},
    {'key': 'secondary_color', 'label': 'Color Secundario', 'value': '#00FF00'},
    {'key': 'success_color', 'label': 'Color Operacion Exitosa', 'value': '#00FF00'},
    {'key': 'warning_color', 'label': 'Color para Advertencia', 'value': '#FFFF00'},
    {'key': 'danger_color', 'label': 'Color para Peligro', 'value': '#FF0000'},
    {'key': 'error_color', 'label': 'Color para Error', 'value': '#FF0000'},
]

def initialize_default_settings():
    if not Settings.query.first():
        for setting in default_settings:
            new_setting = Settings(key=setting['key'], value=setting['value'], label=setting['label'])
            db.session.add(new_setting)
        db.session.commit()

@settings_bp.route('/', methods=['GET', 'POST'])
def config():
    initialize_default_settings()
    settings = Settings.query.all()
    SettingsForm = generate_settings_form(settings)
    form = SettingsForm(request.form)
    
    if form.validate_on_submit():
        for key, value in form.data.items():
            if key == 'csrf_token':
                continue
            setting = Settings.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = Settings(key=key, value=value, label=setting.label)
                db.session.add(setting)
        db.session.commit()
        flash('Settings updated successfully.')
        return redirect(url_for('settings.config'))
    
    return render_template('settings/form.html', form=form, title='Settings')

@settings_bp.route('/add', methods=['GET', 'POST'])
def add_setting():
    if request.method == 'POST':
        key = request.form.get('key')
        value = request.form.get('value')
        label = request.form.get('label')
        
        if key and value and label:
            setting = Settings(key=key, value=value, label=label)
            db.session.add(setting)
            db.session.commit()
            flash('Setting added successfully.')

            return redirect(url_for('settings.config'))
        
    return render_template('settings/add_setting.html', title='Add Setting')