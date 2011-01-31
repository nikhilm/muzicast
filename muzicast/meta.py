import mutagen

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    url = Column(String)
, artist           INTEGER
, album            INTEGER
, genre            INTEGER
, composer         INTEGER
, year             INTEGER -- UNIX time
, title            TEXT
, comment          TEXT
, tracknumber      INTEGER
, discnumber       INTEGER
, bitrate          INTEGER
, duration         INTEGER -- stored as milliseconds
, samplerate       INTEGER
, filesize         INTEGER
, filetype         TEXT
, bpm              REAL
, createdate       INTEGER  -- UNIX time
, modifydate       INTEGER  -- UNIX time
