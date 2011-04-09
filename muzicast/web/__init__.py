import os
import exceptions
from sqlobject import dberrors
from flask import Flask, redirect, url_for, request, current_app, render_template

from muzicast.const import USERDIR
from muzicast.meta import init_meta
from muzicast.web.util import is_first_run

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

def redirect_firstrun():
    if request.path != '/firstrun' and not request.path.startswith('/static/') and not request.path == '/favicon.ico':
        return redirect('/firstrun')

if is_first_run():
    app.before_request(redirect_firstrun)

from muzicast.web.admin import admin
app.register_module(admin, url_prefix='/admin')

from muzicast.web.artist import artist
app.register_module(artist, url_prefix='/artist')
from muzicast.web.album import album
app.register_module(album, url_prefix='/album')
from muzicast.web.track import track
app.register_module(track, url_prefix='/track')
from muzicast.web.genre import genre
app.register_module(genre, url_prefix='/genre')
from muzicast.web.user import user
app.register_module(user, url_prefix='/user')
from muzicast.web.playlist import playlist
app.register_module(playlist, url_prefix='/playlist')
from muzicast.web.search import search
app.register_module(search, url_prefix='/search')

from muzicast.web.main import main
app.register_module(main, url_prefix='/')

@app.route('/firstrun')
def first_run():
    try:
        init_meta()

        #remove hook
        def not_first_run_func(f):
            return f.__name__ != 'redirect_firstrun'

        # NOTE: These two things should be the last things
        # to be done
        app.before_request_funcs[None] = filter(not_first_run_func,
                                                app.before_request_funcs[None])
        return render_template('firstrun/success.html')
    except (OSError, dberrors.Error, exceptions.RuntimeError), e:
        return render_template('firstrun/error.html', error=e.message)

app.secret_key = os.urandom(24)
