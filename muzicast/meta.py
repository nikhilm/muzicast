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
    image = UnicodeCol(default=None)
    tracks = SQLMultipleJoin('Track')

class Genre(SQLObject):
    name = UnicodeCol()

class Composer(SQLObject):
    name = UnicodeCol()

class Track(SQLObject):
    url = UnicodeCol(alternateID=True)
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
    last_played = DateTimeCol(default=DateTimeCol.now)
    play_count = IntCol(default=0)

class AlbumStatistics(SQLObject):
    album = ForeignKey('Album')
    last_played = DateTimeCol(default=DateTimeCol.now)
    play_count = IntCol(default=0)

class ArtistStatistics(SQLObject):
    artist = ForeignKey('Artist')
    last_played = DateTimeCol(default=DateTimeCol.now)
    play_count = IntCol(default=0)

class GenreStatistics(SQLObject):
    genre = ForeignKey('Genre')
    last_played = DateTimeCol(default=DateTimeCol.now)
    play_count = IntCol(default=0)

class User(SQLObject):
    username = UnicodeCol(alternateID=True)
    password = StringCol()
    registered_on = DateTimeCol(default=DateTimeCol.now)
    current_playlist = IntCol(default=-1)

class Playlist(SQLObject):
    user = ForeignKey('User')
    name = StringCol()
    tracks = PickleCol()

def init_meta():
    """
    Creates metadata tables.

    Should be run before any transactions
    are performed.
    NOTE: This should be called only once,
    otherwise it will OVERWRITE the earlier data.
    """
    Artist.createTable(ifNotExists=True)
    Album.createTable(ifNotExists=True)
    Genre.createTable(ifNotExists=True)
    Composer.createTable(ifNotExists=True)
    Track.createTable(ifNotExists=True)
    TrackStatistics.createTable(ifNotExists=True)
    AlbumStatistics.createTable(ifNotExists=True)
    ArtistStatistics.createTable(ifNotExists=True)
    GenreStatistics.createTable(ifNotExists=True)
    User.createTable(ifNotExists=True)
    Playlist.createTable(ifNotExists=True)
    # XXX: Add more HERE
    return True

#TODO(nikhil) statistics, playlists tables
