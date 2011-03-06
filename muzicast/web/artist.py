from flask import Module, render_template, url_for, redirect, session, escape, request, current_app, abort

from muzicast.const import DB_FILE
from muzicast.meta import Artist
from muzicast.web import playlist
from muzicast.web.util import page_view

artist = Module(__name__)

@artist.route('s')
def artists():
    return artists_page(1)

@artist.route('s/<int:page>')
def artists_page(page):
    return page_view(page, Artist, "artists.html", "artists")

@artist.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    artist = Artist.get(id)
    return render_template("artist.html", artist=artist, playlist=playlist)

@artist.route('/add/<int:id>')
def add_artist_to_playlist(id):
    try:
        artist = Artist.get(id)
        for album in artist.albums:
            for track in album.tracks:
                playlist.add_to_playlist(track.id)
        return redirect(request.headers['referer'])
    except LookupError:
        abort(400)
