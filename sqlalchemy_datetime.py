from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, './dbTest.db')
session_options = {'autocommit': False, 'autoflush': False}
db = SQLAlchemy(app, session_options=session_options)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    pub_date = db.Column(db.DateTime)

    def __init__(self, username, email, pub_date):
        self.username = username
        self.email = email
        self.pub_date = pub_date

    def __repr__(self):
        return '<User %r>' % self.username

db.drop_all()
db.create_all()

admin = User('admin', 'admin@example.com', datetime(2015, 6, 5, 8, 10, 10, 10))
guest1 = User('guest1', 'guest1@example.com', datetime(2015, 6, 5, 10, 20, 10, 10))
guest2 = User('guest2', 'guest2@example.com', datetime(2015, 6, 5, 11, 12, 12, 10))

db.session.add(admin)
db.session.add(guest1)
db.session.add(guest2)


users = User.query.all()
print "First: autoflush=False, query dont autoflush, users is:"
print users

db.session.flush()

users = User.query.all()
print "Second: manually flush, query back all info and can get id but not
persist:"
print users
print users[0].id

db.session.commit()

users = User.query.all()
print "Third: committed, data persisted"
print users

admin = User.query.filter_by(username='admin').first()
print admin

user_range = User.query.filter(User.pub_date < datetime(2015, 6, 5, 10, 20, 11), User.pub_date >= datetime(2015, 6, 5, 9, 11 ,11)).all()
print user_range
