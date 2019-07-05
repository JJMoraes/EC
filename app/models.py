from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime, date

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if not self.has_permission(perm):
            self.permission -= perm

    def reset_permission(self):
        self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            'READER': [
                Permission.FOLLOW,
                Permission.COMMENT,
            ],
            'MODERATOR': [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE
            ],
            'ADMINISTRATOR': [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,
                Permission.ADMIN
            ],
            'POSTER':[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE
            ],
        }
        default_role = 'READER'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    about_me = db.Column(db.String(140))
    avatar = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    userStats = db.Column(db.CHAR(1))
    userRole = db.Column(db.Integer, db.ForeignKey('role.id'))
    logs = db.relationship('Log', backref='userLog', lazy=True)
    articles = db.relationship('Article', backref='userAuthor', lazy='dynamic')
    followed = db.relationship(
        'Follow', foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    followers = db.relationship(
        'Follow', foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return '<User %r>' % self.name

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.userRole is None:
            self.userRole = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.name

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

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id
        ).first() is not None

    def is_followed(self, user):
        return self.followers.filter_by(
            follower_id=user.id
        ).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateIn = db.Column(db.DateTime)
    dateOut = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Log %r>' % self.user

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    catColumn = db.Column(db.Boolean, default=False)
    articles = db.relationship('Article', backref="articleCategory", lazy=True)

    def __repr__(self):
        return '<Category %r>' % self.name

    @staticmethod
    def insert_categories():
        categories = ['Politica', 'Filosofia', 'Reflexões', 'Literatura', 'Cinema', 'Música', 'Esportes', 'Tecnologia', 'Saúde']
        for category in categories:
            db.session.add(Category(name=category))
        db.session.commit()


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    date = db.Column(db.Date, default=date.today())
    image = db.Column(db.String(100))
    subtitle = db.Column(db.String(64))
    lide = db.Column(db.String(240))
    text = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    #catColumn = db.Column(db.Integer, db.ForeignKey())

    def __repr__(self):
        return '<Article %r>'%self.title

    @staticmethod
    def insert_articles():
        categories = Category.query.all()
        for category in categories:
            for x in range(4):
                article = Article(
                    title='Masculinidade Frágil - A falácia dos oprimidos opressores. ',
                    image='homem.jpg',
                    subtitle='Homem ajustando a gravata.',
                    lide = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Nulla arcu nunc, pharetra eget porta nec, mattis ut urna. Maecenas \
                    augue erat, iaculis vitae vestibulum eget, maximus sed dui.',
                    text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Nulla arcu nunc, pharetra eget porta nec, mattis ut urna. Maecenas \
                    augue erat, iaculis vitae vestibulum eget, maximus sed dui \
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Nulla arcu nunc, pharetra eget porta nec, mattis ut urna. \
                    Maecenas augue erat, iaculis vitae vestibulum eget, maximus sed dui.',
                    author=1,
                    category=category.id
                )
                db.session.add(article)
        db.session.commit()

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