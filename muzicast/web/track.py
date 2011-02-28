import sqlite3

from flask import Module, render_template, url_for, redirect, session, escape, request, current_app

from muzicast.const import DB_FILE

track = Module(__name__)

@track.route('/<id>')
def index(id):
    conn = sqlite3.Connection(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''select tracks.*,
              albums.id as album_id,
              albums.name as album_name,
              artists.id as artist_id,
              artists.name as artist_name
              from tracks join albums, artists on tracks.album = albums.id and tracks.artist = artists.id where tracks.id=?;''', id)
    r = c.fetchone()
    return render_template("track.html", track=r)
