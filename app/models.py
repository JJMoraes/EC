from app import db

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