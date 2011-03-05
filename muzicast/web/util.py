import os
from flask import render_template

from muzicast import const

def is_first_run():
    return not os.path.exists(const.CONFIG)

def make_pls_playlist(tracks):
    """
    expects a list of meta.Track objects and returns
    a PLS playlist string
    """
    return render_template('pls.txt', tracks=list(tracks))
