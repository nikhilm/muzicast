import os
from flask import render_template, request

from muzicast import const

def is_first_run():
    return not os.path.exists(const.CONFIG)

def make_pls_playlist(tracks):
    """
    expects a list of meta.Track objects and returns
    a PLS playlist string
    """
    url = request.environ['HTTP_HOST']
    pos = url.rfind(':' + request.environ['SERVER_PORT'])
    if pos != -1:
        url = url[:pos]
    # otherwise the host is just the host without a port,
    # which is just what we want
    return render_template('pls.txt', tracks=list(tracks), url=url, port=const.STREAM_PORT)
