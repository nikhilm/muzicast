import os
import sys
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
    name = UnicodeCol()
    albums = MultipleJoin('Album')

class Album(SQLObject):
    name = UnicodeCol()
    artist = ForeignKey('Artist')
    image = UnicodeCol()
    tracks = MultipleJoin('Track')

class Genre(SQLObject):
    name = UnicodeCol()

class Composer(SQLObject):
    name = UnicodeCol()

class Track(SQLObject):
    url = UnicodeCol()
    artist = ForeignKey('Artist')
    album = ForeignKey('Album')
    genre = ForeignKey('Genre')
    composer = ForeignKey('Composer')
    year = IntCol()
    title = UnicodeCol()
    comment = UnicodeCol()
    tracknumber = IntCol()
    discnumber = IntCol()
    bitrate = IntCol()
    duration = IntCol()
    filesize = IntCol()
    filetype = StringCol()
    bpm = IntCol()
    createdate = DateTimeCol()
    modifydate = DateTimeCol()

class TrackStatistics(SQLObject):
    track = ForeignKey('Track')
    last_played = DateTimeCol()
    play_count = IntCol()

class AlbumStatistics(SQLObject):
    album = ForeignKey('Album')
    last_played = DateTimeCol()
    play_count = IntCol()

class ArtistStatistics(SQLObject):
    artist = ForeignKey('Artist')
    last_played = DateTimeCol()
    play_count = IntCol()

class GenreStatistics(SQLObject):
    genre = ForeignKey('Genre')
    last_played = DateTimeCol()
    play_count = IntCol()

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
    TrackStatistics.createTable()
    AlbumStatistics.createTable()
    ArtistStatistics.createTable()
    GenreStatistics.createTable()
    # XXX: Add more HERE
    return True

#TODO(nikhil) statistics, playlists tables
