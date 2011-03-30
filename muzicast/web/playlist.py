from sqlobject.main import SQLObjectNotFound
from flask import Module, render_template, url_for, redirect, session, escape, request, current_app, abort

from muzicast.meta import Track, Playlist, User

playlist = Module(__name__)

def add_to_playlist(tid):
    if 'playlist' not in session:
        session['playlist'] = set()
    print 'adding', tid, session['playlist']
    session['playlist'].add(tid)
    session.modified = True

def delete_from_playlist(tid):
    if 'playlist' not in session:
        return
    session['playlist'].discard(tid)
    session.modified = True

def playlist_contains(tid):
    if 'playlist' not in session:
        return False
    return tid in session['playlist']

def playlist_clear():
    if 'playlist' in session:
        del session['playlist']
    session.modified = True

def playlist_entries():
    if 'playlist' not in session:
        return []
    print session['playlist']
    return (Track.get(id) for id in session['playlist'])

def playlist_name():
    if not 'user' in session:
        return ""
    if session['user']['current_playlist'] == -1:
        return ""
    try:
        pl = Playlist.get(session['user']['current_playlist'])
        return pl.name
    except SQLObjectNotFound:
        return ""

@playlist.route('/save', methods=['POST'])
def save_current():
    if not 'user' in session:
        return redirect(url_for('main.index'))

    user = session['user']
    pl = None
    if user['current_playlist'] == -1:
        # we have to create a new playlist
        pl = Playlist(user=User.byUsername(user['username']), name=request.form['playlist-name'], tracks=set())
    else:
        try:
            pl = Playlist.get(user.current_playlist)
        except SQLObjectNotFound:
            return redirect(url_for('main.index'))
    
    pl.name = request.form['playlist-name']
    pl.tracks = session['playlist']
    pl.sqlmeta.expired = True
    session['user']['current_playlist'] = -1
    if 'playlist' in session:
        del session['playlist']
    session.modified = True
    return redirect(request.headers['referer'])

@playlist.route('/manage')
def manage():
    from muzicast.web.util import render_master_page
    if not 'user' in session:
        return redirect(url_for('main.index'))

    user = User.byUsername(session['user']['username'])
    return render_master_page('playlist-manager.html', title='Manage Playlists', playlists=Playlist.select(Playlist.q.user == user))

@playlist.route('/makeactive/<int:id>')
def set_active(id):
    if 'user' in session:
        try:
            pl = Playlist.get(id)
            if pl.user.username == session['user']['username']:
                session['user']['current_playlist'] = pl.id
                session['playlist'] = pl.tracks
                session.modified = True
            else:
                current_app.logger.debug("Playlist owner is not currently logged in user")
        except SQLObjectNotFound:
            current_app.logger.debug("Playlist %d cannot be set active since it doesn't exist", id)
    return redirect(request.headers['referer'])

@playlist.route('/delete/<int:id>')
def delete(id):
    if 'user' in session:
        try:
            pl = Playlist.get(id)
            if pl.user.username == session['user']['username']:
                if session['user']['current_playlist'] == pl.id:
                    session['user']['current_playlist'] = -1
                    if 'playlist' in session:
                        del session['playlist']
                    session.modified = True
                pl.destroySelf()
            else:
                current_app.logger.debug("Playlist owner is not currently logged in user")
        except SQLObjectNotFound:
            current_app.logger.debug("Playlist %d cannot be deleted since it doesn't exist", id)

    return redirect(request.headers['referer'])
