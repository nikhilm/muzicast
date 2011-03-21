from flask import Module, url_for, redirect, session, escape, request

from muzicast.const import DB_FILE
from muzicast.meta import Genre
from muzicast.web.util import render_master_page

genre = Module(__name__)

@genre.route('s')
def genres():
    return "TODO: fixme"

@genre.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    genre = Genre.get(id)
    return render_master_page("genre.html", title="Genre", genre=genre)
