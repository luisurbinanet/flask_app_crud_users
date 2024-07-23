from faker import Faker
from flask import render_template, redirect, url_for, flash
from . import permissions_bp
from .forms import PermissionForm
from extensions import db
from models import Permission
from utils.helpers import pluralize

model_label = 'Permiso'
plural_model_label = pluralize(model_label)

default_actions = [
    {'name': 'Ver'},
    {'name': 'Crear'},
    {'name': 'Editar'},
    {'name': 'Eliminar'}
]

modules = [
    {'module': 'Usuarios'},
    {'module': 'Roles'},
    {'module': 'Permisos'},
]

combined_list = [f"{action['name']} {module['module']}" for module in modules for action in default_actions]

def initialize_permissions():
    if not Permission.query.first():
        for permission_name in combined_list:
            new_permission = Permission(name=permission_name)
            db.session.add(new_permission)
        db.session.commit()

@permissions_bp.route('/')
def index():
    initialize_permissions()
    permissions = Permission.query.all()
    return render_template('permissions/list.html', permissions=permissions, modelLabel=model_label, pluralModelLabel=plural_model_label)

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
    return render_template('permissions/form.html', form=form, action='Crear', modelLabel=model_label, pluralModelLabel=plural_model_label)

@permissions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    permission = Permission.query.get_or_404(id)
    form = PermissionForm(obj=permission)
    if form.validate_on_submit():
        form.populate_obj(permission)
        db.session.commit()
        flash('Permission updated successfully.')
        return redirect(url_for('permissions.index'))
    return render_template('permissions/form.html', form=form, action='Editar', modelLabel=model_label, pluralModelLabel=plural_model_label)

@permissions_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    flash('Permission deleted successfully.')
    return redirect(url_for('permissions.index'))
