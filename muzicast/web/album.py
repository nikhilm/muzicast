from flask import Module, render_template, url_for, redirect, session, escape, request, abort

from muzicast.const import DB_FILE
from muzicast.meta import Album
from muzicast.web import playlist
from muzicast.web.util import page_view

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
    return render_template("album.html", album=album, playlist=playlist)
