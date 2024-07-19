from flask import render_template, redirect, url_for, flash
from . import permissions_bp
from .forms import PermissionForm
from models import db, Permission

module = 'Permisos'

@permissions_bp.route('/')
def index():
    permissions = Permission.query.all()
    return render_template('permissions/list.html', permissions=permissions, breadcrumb_title=module)

@permissions_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PermissionForm()
    if form.validate_on_submit():
        permission = Permission(
            name=form.name.data
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permission created successfully.')
        return redirect(url_for('permissions.index'))
    return render_template('permissions/form.html', form=form, title='Create Permission', breadcrumb_title=module)

@permissions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    permission = Permission.query.get_or_404(id)
    form = PermissionForm(obj=permission)
    if form.validate_on_submit():
        form.populate_obj(permission)
        db.session.commit()
        flash('Permission updated successfully.')
        return redirect(url_for('permissions.index'))
    return render_template('permissions/form.html', form=form, title='Edit Permission', breadcrumb_title=module)

@permissions_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    flash('Permission deleted successfully.')
    return redirect(url_for('permissions.index'))
