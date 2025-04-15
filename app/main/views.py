 from flask import session, render_template, redirect, url_for, flash, request

from . import main
from .. import db
from ..models import User, Entertainment, Playlist
from .forms import *
from flask_login import login_required, current_user, login_user, logout_user


@main.route("/")
def index():
    return render_template ("index.html", title="Home")

@main.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('main.index'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid username or password")
    return render_template("login.html", form=form, title = "Login")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))

@main.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in and signed up.")
        return redirect(url_for('main.index'))
    
    form = UserForm()

    if(form.validate_on_submit()):
        username = form.username.data
        pw = form.password.data
        email = form.email.data
        created = createUser(username, pw, email)
        if(created):
            flash("Registered user " + username)
        else:
            flash("User already exists with username " + username)
        return redirect(Url_for('main.index'))

    return render_template("register.html", form = form, title = "Create Account")

def createUser(username, password, email):
    u = User.query.filter_by(username=username).first()
    if(u == None):
        user = User(username = username, password = password, email = email)
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False

def addEnt(medium, title, genre):
    ent = Entertainment(medium = medium, title = title, genre = genre)
    db.session.add(ent)
    db.session.commit()

def addMusic(title, artist, genre):
    music = Playlist(title = title, artist = artist, genre = genre)
    db.session.add(music)
    db.session.commit()
