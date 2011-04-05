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

def page_view(page, cls, template, key, per_page=5, **kw):
    """
    Creates a paging system to allow browsing
    larger data sets.

    page is the current page to be shown
    cls is the ORM instance whose rows are displayed
    template is the template that is to be rendered as the main page
    key is the name the template expects the results to be as
    per_page is the number of results shown per page
    kw are keyword arguments passed on to render_master_page, useful for plugging in other things.
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
    kwargs.update(kw)
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
