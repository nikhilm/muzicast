import os
import sys
from sqlobject import *

from flask import Module, url_for, redirect, session, escape, request, abort, current_app, send_file

from muzicast.const import DB_FILE
from muzicast.web.util import page_view, render_master_page
from muzicast.meta import Artist,Album,Genre,Composer,Track

search = Module(__name__)

def Artist_Search(keylist):
    artist=[]
    for keyword in keylist:
        #tmp= Track.select(AND(Artist.q.name.contains(keyword),Artist.q.id==Track.q.artist))
        tmp= Artist.select(Artist.q.name.contains(keyword))
        artist.extend(tmp)
    artist=set(artist)
    return artist

def Album_Search(keylist):
    album=[]
    for keyword in keylist:
        #tmp= Track.select(AND(Album.q.name.contains(keyword),Album.q.id==Track.q.album))
        tmp= Album.select(Album.q.name.contains(keyword))
        album.extend(tmp)
    album=set(album)
    return album

def Genre_Search(keylist):
    genre=[]
    for keyword in keylist:
        #tmp= Track.select(AND(Genre.q.name.contains(keyword),Genre.q.id==Track.q.genre))
        tmp= Genre.select(Genre.q.name.contains(keyword))
        genre.extend(tmp)
    genre=set(genre)
    return genre

def Composer_Search(keylist):
    composer=[]
    for keyword in keylist:
        #tmp= Track.select(AND(Composer.q.name.contains(keyword),Composer.q.id==Track.q.composer))
        tmp= Composer.select(Composer.q.name.contains(keyword))
        composer.extend(tmp)
    composer=set(composer)
    return composer

def Track_Search(keylist):
    track=[]
    for keyword in keylist:
        tmp= Track.select(Track.q.title.contains(keyword))
        track.extend(tmp)
    track=set(track)
    return track

@search.route('/')
def index():
    query = request.args.get('query', '')
    keylist = query.split()
    return render_master_page("search_results.html", title="Results for \"%s\""%query, results={
        'artists': Artist_Search(keylist),
        'albums' : Album_Search(keylist),
        'tracks' : Track_Search(keylist)
    })
