import os
from sqlobject import *

from muzicast.const import DB_FILE

# NOTE: When adding a class to this file, make a relevant
# entry in init_meta to initialize the database
connection_string = 'sqlite://' + DB_FILE
if sys.platform == 'win32':
    connection_string = 'sqlite:/' + os.path.normpath(DB_FILE).replace(':', '|/', 1)

connection = connectionForURI(connection_string)
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

def init_meta():
    """
    Creates metadata tables.

    Should be run before any transactions
    are performed.
    NOTE: This should be called only once,
    otherwise it will OVERWRITE the earlier data.
    """
    Artist.createTable()
    Album.createTable()
    Genre.createTable()
    Composer.createTable()
    Track.createTable()
    # XXX: Add more HERE
    return True

#TODO(nikhil) statistics, playlists tables
