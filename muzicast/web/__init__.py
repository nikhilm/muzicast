import os
from flask import Flask

app = Flask(__name__)

from muzicast.web.admin import admin
app.register_module(admin, url_prefix='/admin')

#from muzicast.web.music import artist, album, track
#app.register_module(artist, url_prefix='/artist')
#app.register_module(album, url_prefix='/album')
#app.register_module(track, url_prefix='/track')

from muzicast.web.main import main
app.register_module(main, url_prefix='/')

app.secret_key = os.urandom(24)
