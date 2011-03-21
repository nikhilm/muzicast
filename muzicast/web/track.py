from flask import Module, render_template, url_for, redirect, session, escape, request, current_app, abort

from muzicast.const import DB_FILE
from muzicast.meta import Track
from muzicast.web import playlist
from muzicast.web.util import render_master_page

track = Module(__name__)

@track.route('s')
def tracks():
    return "TODO: fixme"

@track.route('/<int:id>')
def index(id):
    track = Track.get(id)
    return render_master_page("track.html", title='Muzicast: Track', track=track)

@track.route('/add/<int:id>')
def add_track_to_playlist(id):
    playlist.add_to_playlist(id)
    return redirect(request.headers['referer'])

@track.route('/delete/<int:id>')
def delete_track_from_playlist(id):
    playlist.delete_from_playlist(id)
    return redirect(request.headers['referer'])
