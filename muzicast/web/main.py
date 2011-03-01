from flask import Module, render_template, url_for, redirect, session, escape, request

from muzicast.web.util import is_first_run
from muzicast.meta import Track

main = Module(__name__)

def top_tracks(n):
    """
    Returns the top n tracks
    """
    #TODO(nikhil) fix this to use statistics
    return [Track.get(i) for i in range(1, n+1)]

def recently_played(n):
    """
    Returns n latest played tracks
    """
    #TODO(nikhil) fix this to use statistics
    return [Track.get(i) for i in range(1, n+1)]

@main.route('/')
def index():
    #just do first run check
    if is_first_run():
        return redirect(url_for('admin.index'))

    # TODO: will need attributes for template
    return render_template('home.html', top_tracks=top_tracks, recently_played=recently_played)
