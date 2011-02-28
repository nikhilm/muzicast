import sqlite3

from flask import Module, render_template, url_for, redirect, session, escape, request, current_app

from muzicast.const import DB_FILE

artist = Module(__name__)

@artist.route('/<id>')
def index(id):
    conn = sqlite3.Connection(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''select * from artists where id=?;''', id)
    return render_template("artist.html", track=c.fetchone())
