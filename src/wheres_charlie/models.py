from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin
from flask_marshmallow import Marshmallow

from . import app

db = SQLAlchemy(app)
ma = Marshmallow(app)

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
    locations = db.relationship('Location', back_populates='user')


class Location(db.Model):
    location_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    user = db.relationship('User')
    location_string = db.Column(db.String(255))
    date_time = db.Column(db.Date())
    active = db.Column(db.Boolean())


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('password',)


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
