import sqlite3

from flask import Module, render_template, url_for, redirect, session, escape, request, current_app

from muzicast.const import DB_FILE
from muzicast.meta import Track

track = Module(__name__)

@track.route('/<id>')
def index(id):
    track = Track.get(id)
    return render_template("track.html", track=track)
