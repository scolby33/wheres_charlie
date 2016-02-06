from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin

from . import app

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id')))


class Role(db.Model, RoleMixin):
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Location(db.Model):
    location_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    location_string = db.Column(db.String(255))
    date_time = db.Column(db.Date())
    active = db.Column(db.Boolean())
