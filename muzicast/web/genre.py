from flask import Module, render_template, url_for, redirect, session, escape, request

from muzicast.const import DB_FILE
from muzicast.meta import Genre
from muzicast.web import playlist

genre = Module(__name__)

@genre.route('s')
def genres():
    return "TODO: fixme"

@genre.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    genre = Genre.get(id)
    return render_template("genre.html", genre=genre, playlist=playlist)
