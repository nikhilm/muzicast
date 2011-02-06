import mutagen

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    artist = relationship("Artist", backref="track")
    album = relationship("Album", backref="track")
    genre = relationship("Genre", backref="track")
    composer = relationship("Composer", backref="track")
    year = Integer()
    title = String()
    comment = String()
    tracknumber = Integer()
    discnumber = Integer()
    bitrate = Integer()
    duration = Integer()
    samplerate = Integer()
    filesize = Integer()
    filetype = String()
    bpm = Integer()
    createdate = DateTime()
    modifydate = DateTime()
