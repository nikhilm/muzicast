from flask import Module, render_template, url_for, redirect, session, escape, request, current_app, abort

from muzicast.const import DB_FILE
from muzicast.meta import Track
from muzicast.web import playlist

track = Module(__name__)

@track.route('s')
def tracks():
    return "TODO: fixme"

@track.route('/<int:id>')
def index(id):
    track = Track.get(id)
    return render_template("track.html", track=track, playlist=playlist)

@track.route('/add/<int:id>')
def add_track_to_playlist(id):
    playlist.add_to_playlist(id)
    return redirect(request.headers['referer'])

@track.route('/delete/<int:id>')
def delete_track_from_playlist(id):
    playlist.delete_from_playlist(id)
    return redirect(request.headers['referer'])
