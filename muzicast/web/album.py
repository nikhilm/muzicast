import sqlite3

from flask import Module, render_template, url_for, redirect, session, escape, request

from muzicast.const import DB_FILE

album = Module(__name__)

@album.route('/<id>')
def index(id):
    conn = sqlite3.Connection(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''select * from albums where id=?;''', id)
    return render_template("album.html", track=c.fetchone())
