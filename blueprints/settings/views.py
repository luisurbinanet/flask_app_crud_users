from flask import render_template, redirect, url_for, flash
from . import settings_bp
from .forms import SettingsForm
from models import db, Settings

@settings_bp.route('/config', methods=['GET', 'POST'])
def config():
    settings = Settings.query.first()
    form = SettingsForm(obj=settings)
    if form.validate_on_submit():
        if settings is None:
            settings = Settings()
        form.populate_obj(settings)
        db.session.add(settings)
        db.session.commit()
        flash('Settings updated successfully.')
    return render_template('settings/form.html', form=form, title='Settings')
