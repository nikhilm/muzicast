from flask import Module, render_template, url_for, redirect, session, escape, request

from muzicast.const import DB_FILE
from muzicast.meta import Album
from muzicast.web import playlist

album = Module(__name__)

@album.route('s')
def albums():
    return "TODO: fixme"

@album.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    album = Album.get(id)
    return render_template("album.html", album=album, playlist=playlist)
