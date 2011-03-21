from flask import Module, url_for, redirect, session, escape, request, make_response

from sqlobject.main import SQLObjectNotFound

from muzicast.web.util import is_first_run, make_pls_playlist, render_master_page
from muzicast.meta import Track
from muzicast.web import playlist

main = Module(__name__)

def top_tracks(n):
    """
    Returns the top n tracks
    """
    #TODO(nikhil) fix this to use statistics
    try:
        return [Track.get(i) for i in range(1, n+1)]
    except SQLObjectNotFound:
        return []

def recently_played(n):
    """
    Returns n latest played tracks
    """
    #TODO(nikhil) fix this to use statistics
    try:
        return [Track.get(i) for i in range(1, n+1)]
    except SQLObjectNotFound:
        return []

@main.route('/')
def index():
    #just do first run check
    if is_first_run():
        return redirect(url_for('admin.index'))

    # TODO: will need attributes for template
    return render_master_page('home.html', title='Muzicast', top_tracks=top_tracks, recently_played=recently_played)

@main.route('playlist/download/playlist.pls')
def download_playlist():
    pls = make_pls_playlist(playlist.playlist_entries())
    response = make_response(pls, None, None, 'audio/x-scpls')
    return response

@main.route('playlist/clear')
def clear_playlist():
    playlist.playlist_clear()
    return redirect(request.headers['referer'])
