from flask import render_template, redirect, url_for, flash
from . import users_bp
from .forms import UserForm
from models import db, User

@users_bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@users_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            avatar=form.avatar.data,
            role_id=form.role_id.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.')
        return redirect(url_for('users.index'))
    return render_template('users/form.html', form=form, title='Create User')

@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('users.index'))
    return render_template('users/form.html', form=form, title='Edit User')

@users_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('users.index'))
