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
        return redirect(url_for('main.index'))

    return render_template("register.html", form = form, title = "Create Account")

@main.route("/addfunstuff", methods = ["GET", "POST"])
@login_required
def addfunstuff():
    form = FunForm()

    if(form.validate_on_submit()):
        medium = form.medium.data
        title = form.title.data
        genre = form.genre.data
        user_id = current_user.id
        addFunThing(medium, title, genre, user_id)
        return redirect(url_for("main.my_fun_stuff"))
    
    return render_template("addfunthing.html", form = form, title = "Add Fun Thing")

@main.route("/addmusic", methods = ["GET", "POST"])
@login_required
def addmusic():
    form = PlaylistForm()

    if (form.validate_on_submit()):
        title = form.title.data
        artist = form.artist.data
        genre = form.genre.data
        user_id = current_user.id

        addMusic(title, artist, genre, user_id)
        flash("Music Added to Playlist")
        return redirect(url_for("main.my_music"))

    return render_template("addmusic.html", form = form, title = "Add Music")

@main.route("/myfunstuff")
@login_required
def my_fun_stuff():

    fun = Entertainment.query.filter_by(user_id = current_user.id).all()

    return render_template("entertainment.html", fun = fun, title = "My Fun Stuff")

@main.route("/mymusic", methods = ["POST", "GET"]) 
# added post get to see something
@login_required
def my_music():

    playlist = Playlist.query.filter_by(user_id = current_user.id).all()

    return render_template("playlist.html", playlist = playlist, title = "My Music Playlist" )

@main.route("/deletefun/<int:id>", methods = ["POST"])
@login_required
def deletefunthing(id):

    funthing = Entertainment.query.filter_by(user_id=current_user.id, id = id).first()

    db.session.delete(funthing)
    db.session.commit()
    flash("You have deleted fun thing.")

    return redirect(url_for("main.my_fun_stuff"))

@main.route("/deletemusic/<int:id>", methods = ["GET", "POST"])
@login_required
def deletemusic(id):

    music = Playlist.query.filter_by(id = id).first()

    db.session.delete(music)
    db.session.commit()
    flash("You deleted song from your playlist")

    return redirect(url_for("main.my_music"))


def createUser(username, password, email):
    u = User.query.filter_by(username=username).first()
    if(u == None):
        user = User(username = username, password = password, email = email)
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


def addFunThing(medium, title, genre, user_id):
    ent = Entertainment(medium = medium, title = title, genre = genre, user_id = user_id)
    db.session.add(ent)
    db.session.commit()

def addMusic(title, artist, genre, user_id):
    music = Playlist(title = title, artist = artist, genre = genre, user_id = user_id)
    db.session.add(music)
    db.session.commit()
