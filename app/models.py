from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique = True)

    def __repr__(self):
        return "<user %r>" % self.username

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Entertainment(db.Model):
    __tablename__ = "entertainments"
    id = db.Column(db.Integer, primary_key=True)
    medium = db.Column(db.String(64), index=True)
    title = db.Column(db.String(64), index=True)
    genre = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index = True)



    def __repr__(self):
        return self.medium + " " + self.title

class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    artist = db.Column(db.String(64), index=True)
    genre = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index = True)


    def __repr__(self):
        return self.title + " " + self.artist + " " + self.genre

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    