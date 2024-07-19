from extensions import db

roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='users')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')
    users = db.relationship('User', secondary=roles_permissions, back_populates='permissions')
