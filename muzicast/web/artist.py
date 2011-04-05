from sqlobject import DESC
from sqlobject.main import SQLObjectNotFound
from flask import Module, render_template, url_for, redirect, session, escape, request, current_app, abort

from muzicast.const import DB_FILE
from muzicast.meta import Artist, ArtistStatistics
from muzicast.web import playlist
from muzicast.web.util import page_view, render_master_page

artist = Module(__name__)

def top_artists(n):
    try:
        return [t.artist for t in ArtistStatistics.select(orderBy=DESC(ArtistStatistics.q.play_count))[:10]]
    except SQLObjectNotFound:
        return []

@artist.route('s')
def artists():
    return artists_page(1)

@artist.route('s/<int:page>')
def artists_page(page):
    return page_view(page, Artist, "artists.html", "artists", top_artists=top_artists(10))

@artist.route('/<id>')
def index(id):
    try:
        artist = Artist.get(id)
        return render_master_page("artist.html", title="Artist", artist=artist)
    except SQLObjectNotFound:
        abort(404)

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
