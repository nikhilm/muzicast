from sqlobject.main import SQLObjectNotFound
from flask import Module, render_template, url_for, redirect, session, escape, request, current_app, abort

from muzicast.const import DB_FILE, STREAM_PORT
from muzicast.meta import Track, TrackStatistics
from muzicast.web import playlist
from muzicast.web.util import page_view, render_master_page

track = Module(__name__)

@track.route('s')
def tracks():
    return tracks_page(1)

@track.route('s/<int:page>')
def tracks_page(page):
    return page_view(page, Track, "tracks.html", "tracks", 20, title='Tracks')

@track.route('/<int:id>')
def index(id):
    try:
        track = Track.get(id)
        stats = list(TrackStatistics.select(TrackStatistics.q.track == track.id))
        if len(stats) > 0:
        	stats = stats[0]
        else:
        	stats = None

        url = request.environ['HTTP_HOST']
        pos = url.rfind(':' + request.environ['SERVER_PORT'])
        if pos != -1:
            url = url[:pos]
        # otherwise the host is just the host without a port,
        # which is just what we want
        return render_master_page("track.html", title='Muzicast: Track', track=track, url=url, port=STREAM_PORT, stats=stats)
    except SQLObjectNotFound:
        abort(404)

@track.route('/add/<int:id>')
def add_track_to_playlist(id):
    playlist.add_to_playlist(id)
    return redirect(request.headers['referer'])

@track.route('/delete/<int:id>')
def delete_track_from_playlist(id):
    playlist.delete_from_playlist(id)
    return redirect(request.headers['referer'])
