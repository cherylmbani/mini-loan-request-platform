from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
#from sqlalchemy.schema import Metadata
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func

from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy


db=SQLAlchemy()
bcrypt =Bcrypt()
migrate=Migrate()
#metadata=Metadata()

class User(db.Model, SerializerMixin):
    __tablename__="users"
    serialize_rules=('-loans.user',)
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, nullable=False)
    email=db.Column(db.Text, nullable=False)
    #phone_number=db.Column(db.Integer, nullable=False)
    _password_hash=db.Column('password', db.Text, nullable=False)
    loans=db.relationship('Loan', back_populates="user")


    @property
    def password(self):
        raise AttributeError("Password is write-only")
    
    @password.setter
    def password(self, password):
        pw_hash=bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash=pw_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))



    def __repr__(self):
        return f"<{self.id} {self.first_name} {self.last_name}>"


class Loan(db.Model, SerializerMixin):
    __tablename__="loans"
    serialize_rules=('-user.loans',)
    id=db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Integer)
    loan_type=db.Column(db.String)
    created_at=db.Column(db.DateTime, default=func.now())
    updated_at=db.Column(db.DateTime, default=func.now())
    application_status=db.Column(db.String)
    reason=db.Column(db.Text)
    # relationship is one user can apply many loans
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    user=db.relationship('User', back_populates="loans")


    def __repr__(self):
        return f"<{self.id} {self.loan_type}>"





