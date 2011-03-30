import os
from math import ceil
from flask import render_template, request, abort

from muzicast import const
from muzicast.web import playlist

def is_first_run():
    return not os.path.exists(const.CONFIG)

def render_master_page(body_page, **kwargs):
    page_data = {
        'playlist': playlist,
        'body_page': body_page,
    }

    page_data.update(kwargs)
    return render_template('master.html', **page_data)

def page_view(page, cls, template, key, per_page=5):
    """
    TODO: document this
    """
    if page < 1:
        return abort(400)
    query = cls.select()
    insts = query[(page-1)*per_page:page*per_page]

    kwargs = {
        'current_page': page,
        'pages'       : int(ceil(query.count()*1.0/per_page)),
        key           : insts
    }
    return render_master_page(template, **kwargs)

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
