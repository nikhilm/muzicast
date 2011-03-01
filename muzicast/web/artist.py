import sqlite3

from flask import Module, render_template, url_for, redirect, session, escape, request, current_app

from muzicast.const import DB_FILE
from muzicast.meta import Artist

artist = Module(__name__)

@artist.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    artist = Artist.get(id)
    return render_template("artist.html", artist=artist)
