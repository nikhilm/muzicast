import os
from flask import Flask

app = Flask(__name__)

from muzicast.web.admin import admin
app.register_module(admin, url_prefix='/admin')

app.secret_key = os.urandom(24)
