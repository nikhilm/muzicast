from flask import Module, url_for, redirect, session, escape, request, make_response

from sqlobject.main import SQLObjectNotFound
from sqlobject import DESC

from muzicast.web.util import is_first_run, make_pls_playlist, render_master_page
from muzicast.meta import Track, TrackStatistics
from muzicast.web.playlist import playlist_clear, playlist_entries

main = Module(__name__)

def top_tracks(n):
    """
    Returns the top n tracks
    """
    try:
        return [t.track for t in TrackStatistics.select(orderBy=DESC(TrackStatistics.q.play_count))[:10]]
    except SQLObjectNotFound:
        return []

def recently_played(n):
    """
    Returns n latest played tracks
    """
    try:
        return [t.track for t in TrackStatistics.select(orderBy=DESC(TrackStatistics.q.last_played))[:10]]
    except SQLObjectNotFound:
        return []

@main.route('/')
def index():
    #just do first run check
    if is_first_run():
        return redirect(url_for('admin.index'))

    return render_master_page('home.html', title='Muzicast', top_tracks=top_tracks, recently_played=recently_played)

@main.route('playlist/download/playlist.pls')
def download_playlist():
    pls = make_pls_playlist(playlist_entries())
    response = make_response(pls, None, None, 'audio/x-scpls')
    return response

@main.route('playlist/clear')
def clear_playlist():
    playlist_clear()
    return redirect(request.headers['referer'])
