from portfolio import db
from flask_login import LoginManager, UserMixin
from portfolio import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    skills = db.relationship('Skills', backref='author', lazy=True)
    testimony = db.relationship('Testimonial', backref='author', lazy=True)
    project = db.relationship('Project', backref='author', lazy=True)
    job = db.relationship('Job', backref='author', lazy=True)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    desc = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='recom.jpg')
    testimony = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sk_name = db.Column(db.String(20), unique=True, nullable=False)
    sk_value = db.Column(db.Integer, nullable=False)
    sk_type = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(50), unique=True, nullable=False)
    p_description = db.Column(db.String(200), unique=True, nullable=True)
    Organization = db.Column(db.String(200), unique=False, nullable=True)
    p_url = db.Column(db.String(200), unique=True, nullable=True)
    cred_id = db.Column(db.String(200), unique=True, nullable=True)
    certi_url = db.Column(db.String(200), unique=True, nullable=True)
    proj_type = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), unique=False, nullable=False)
    company = db.Column(db.String(30), unique=False, nullable=False)
    start = db.Column(db.DateTime, unique=False, nullable=True)
    end = db.Column(db.DateTime, unique=False, nullable=True)
    place = db.Column(db.String(30), unique=False, nullable=True)
    jd = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
