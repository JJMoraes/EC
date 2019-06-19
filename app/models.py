from app import db
from werkzeug.security import check_password_hash, generate_password_hash

from . import login_manager

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = db.Column(db.String(16))
    user = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return '<Role %r>' % self.description


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    userStats = db.Column(db.CHAR(1))
    userRole = db.Column(db.Integer, db.ForeignKey('role.id'))
    logs = db.relationship('Log', backref='user', lazy=True)
    articles = db.relationship('Article', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.has_permission(Permission.ADMIN)


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateIn = db.Column(db.DateTime)
    dateOut = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Log %r>' % self.user


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    date = db.Column(db.Date)
    image = db.Column(db.String(100))
    lide = db.Column(db.String(240))
    text = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Article %r>' % self.title


class AdSense(db.Model):
    __tablename__ = 'adSense'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(100))
    description = db.Column(db.String(64))
    dateInsert = db.Column(db.DateTime)
    adSenseStats = db.Column(db.CHAR(1))

    def __repr__(self):
        return '<AdSense %r>'%self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))