from flask import render_template, redirect, url_for, flash, request
from . import users_bp
from .forms import UserForm
from models import db, User, Role, Permission
from werkzeug.security import generate_password_hash, check_password_hash

module = 'Usuarios'

@users_bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/list.html', users=users, breadcrumb_title=module)

@users_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            avatar=form.avatar.data,
            role_id=form.role_id.data
        )
        db.session.add(user)
        db.session.commit()
        user.permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        db.session.commit()
        flash('User created successfully.')
        return redirect(url_for('users.index'))
    return render_template('users/form.html', form=form, title='Crear Usuario', breadcrumb_title=module)

@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.password.data:  # Solo hashear la contraseña si se proporciona una nueva
            user.password = generate_password_hash(form.password.data, method='sha256')
        user.permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('users.index'))
    form.role_id.data = user.role_id
    form.permissions.data = [perm.id for perm in user.permissions]
    return render_template('users/form.html', form=form, title='Edit User', breadcrumb_title=module)

@users_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('users.index'))
