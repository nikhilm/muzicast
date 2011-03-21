from flask import session

from muzicast.meta import Track

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
    del session['playlist']
    session.modified = True

def playlist_entries():
    if 'playlist' not in session:
        return []
    print session['playlist']
    return (Track.get(id) for id in session['playlist'])
