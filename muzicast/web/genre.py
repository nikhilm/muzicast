from sqlobject import DESC
from sqlobject.main import SQLObjectNotFound
from flask import Module, url_for, redirect, session, escape, request

from muzicast.const import DB_FILE
from muzicast.meta import Genre, GenreStatistics
from muzicast.web import playlist
from muzicast.web.util import render_master_page, page_view

genre = Module(__name__)

def top_genres(n):
    try:
        return [t.genre for t in GenreStatistics.select(orderBy=DESC(GenreStatistics.q.play_count))[:10]]
    except SQLObjectNotFound:
        return []

@genre.route('s')
def genres():
    return genres_page(1)

@genre.route('s/<int:page>')
def genres_page(page):
    return page_view(page, Genre, "genres.html", "genres", top_genres=top_genres(10))

@genre.route('/<id>')
def index(id):
    #TODO(nikhil) handle exception
    genre = Genre.get(id)
    return render_master_page("genre.html", title="genre", genre=genre)

@genre.route('/add/<int:id>')
def add_genre_to_playlist(id):
    try:
        genre = Genre.get(id)
        for track in genre.tracks:
            playlist.add_to_playlist(track.id)
        return redirect(request.headers['referer'])
    except LookupError:
        abort(400)
