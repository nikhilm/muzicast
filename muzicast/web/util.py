import os
from math import ceil
from flask import render_template, request, abort

from muzicast import const
from muzicast.web import playlist

def is_first_run():
    return not os.path.exists(const.CONFIG)

def page_view(page, cls, template, key):
    """
    TODO: document this
    """
    PER_PAGE = 5
    if page < 1:
        return abort(400)
    query = cls.select()
    insts = query[(page-1)*PER_PAGE:page*PER_PAGE]

    kwargs = {
        'playlist'    : playlist,
        'current_page': page,
        'pages'       : int(ceil(query.count()*1.0/PER_PAGE)),
        key           : insts
    }
    return render_template(template, **kwargs)

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
