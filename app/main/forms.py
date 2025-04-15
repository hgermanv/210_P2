from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo

class UserForm(FlaskForm):
    username = StringField("Username: ", validators = [DataRequired()])
    password = PasswordField("Password: ", validators = [DataRequired()])
    email = EmailField("example@mail.com", validators = [DataRequired()])
    confirm = PasswordField("Repeat Password: ", validators = [DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators = [DataRequired()])
    password = PasswordField("Password: ", validators = [DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")

class FunForm(FlaskForm):
    medium = StringField("Medium: ", validators = [DataRequired()])
    title = StringField("Title: ", validators = [DataRequired()])
    genre = StringField("Genre: ", validators = [DataRequired()])
    submit = SubmitField("Add Time Waster")

class Playlist(FlaskForm):
    title = StringField("Title: ", validators = [DataRequired()])
    artist = StringField("Artist: ", validators = [DataRequired()])
    genre = StringField("Genre: ", validators = [DataRequired()])
