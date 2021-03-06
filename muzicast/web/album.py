from sqlobject import DESC
from sqlobject.main import SQLObjectNotFound
from flask import Module, url_for, redirect, session, escape, request, abort, current_app, send_file

from muzicast.const import DB_FILE
from muzicast.meta import Album, AlbumStatistics, Track
from muzicast.web import playlist
from muzicast.web.util import page_view, render_master_page

album = Module(__name__)

def top_albums(n):
    try:
        top = [t.album for t in AlbumStatistics.select(orderBy=DESC(AlbumStatistics.q.play_count))[:n]]
        if len(top) < n:
            top = top + [album for album in Album.select()[:n-len(top)] if album not in top]
        return top
    except SQLObjectNotFound:
        return []

@album.route('s')
def albums():
    return albums_page(1)

@album.route('s/<int:page>')
def albums_page(page):
    return page_view(page, Album, "albums.html", "albums", top_albums=top_albums(10), title='Albums')

@album.route('/<id>')
def index(id):
    try:
        album = Album.get(id)
        return render_master_page("album.html", title="Album", album=album)
    except SQLObjectNotFound:
        abort(400)

@album.route('/add/<int:id>')
def add_album_to_playlist(id):
    try:
        album = Album.get(id)
        for track in album.tracks:
            playlist.add_to_playlist(track.id)
        return redirect(request.headers['referer'])
    except LookupError:
        abort(400)

@album.route('/cover/<int:id>')
def cover(id):
    try:
        album = Album.get(id)
        if not album.image:
            return redirect(url_for('.static', filename='images/nocover.png'))
        return send_file(album.image)
    except LookupError:
        abort(400)
