import os
from sqlobject import *

from muzicast.const import DB_FILE

#TODO(nikhil) handle windows sqlobject alternate drive syntax
#TODO(nikhil) first run should create all tables
connection = connectionForURI('sqlite://' + DB_FILE)
sqlhub.processConnection = connection

class Artist(SQLObject):
    name = StringCol()
    albums = MultipleJoin('Album')

class Album(SQLObject):
    name = StringCol()
    artist = ForeignKey('Artist')
    image = StringCol()
    tracks = MultipleJoin('Track')

class Genre(SQLObject):
    name = StringCol()

class Composer(SQLObject):
    name = StringCol()

class Track(SQLObject):
    url = StringCol()
    artist = ForeignKey('Artist')
    album = ForeignKey('Album')
    genre = ForeignKey('Genre')
    composer = ForeignKey('Composer')
    year = IntCol()
    title = StringCol()
    comment = StringCol()
    tracknumber = IntCol()
    discnumber = IntCol()
    bitrate = IntCol()
    duration = IntCol()
    filesize = IntCol()
    filetype = StringCol()
    bpm = IntCol()
    createdate = DateTimeCol()
    modifydate = DateTimeCol()

#TODO(nikhil) statistics, playlists tables
