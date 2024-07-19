from flask import render_template, redirect, url_for, flash
from . import roles_bp
from .forms import RoleForm
from models import db, Role

module = 'Roles'

@roles_bp.route('/')
def index():
    roles = Role.query.all()
    return render_template('roles/list.html', roles=roles, breadcrumb_title=module)

@roles_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(
            name=form.name.data
        )
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully.')
        return redirect(url_for('roles.index'))
    return render_template('roles/form.html', form=form, title='Crear Rol', breadcrumb_title=module)

@roles_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        form.populate_obj(role)
        db.session.commit()
        flash('Role updated successfully.')
        return redirect(url_for('roles.index'))
    return render_template('roles/form.html', form=form, title='Editar Rol', breadcrumb_title=module)

@roles_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('Role deleted successfully.')
    return redirect(url_for('roles.index'))
