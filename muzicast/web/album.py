from flask import Module, url_for, redirect, session, escape, request, abort, current_app, send_file

from muzicast.const import DB_FILE
from muzicast.meta import Album
from muzicast.web import playlist
from muzicast.web.util import page_view, render_master_page

album = Module(__name__)

@album.route('s')
def albums():
    return albums_page(1)

@album.route('s/<int:page>')
def albums_page(page):
    return page_view(page, Album, "albums.html", "albums")

@album.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    album = Album.get(id)
    return render_master_page("album.html", title="Album", album=album)

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
        current_app.logger.debug('Album cover for %s', album.image)
        if not album.image:
            return redirect(url_for('.static', filename='images/nocover.png'))
        return send_file(album.image)
    except LookupError:
        abort(400)
