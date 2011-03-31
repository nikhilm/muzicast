import asyncore
import BaseHTTPServer
import os
import sys
import signal
import socket
from datetime import datetime
import time
import sqlobject
import re

from muzicast.const import DB_FILE
from muzicast.meta import Track, TrackStatistics, AlbumStatistics, ArtistStatistics, GenreStatistics

route_regex = re.compile(r'/([0-9]*)(;\.mp3)?$')

class StreamJob(BaseHTTPServer.BaseHTTPRequestHandler):
#    def __init__(self, socket, addr, server):
#        #asyncore.dispatcher_with_send.__init__(self, socket)
#        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, socket, addr, server)

    def get_track(self, id):
        """
        Get track meta-data given a track ID.
        Returns {} in case of failure
        """
        try:
            track = Track.get(id)
            return track
        except sqlobject.main.SQLObjectNotFound:
            return None

    def do_GET(self):
        match = route_regex.match(self.path)
        if match:
            self.stream_song(match.group(1))
        else:
            self.send_error(404)

    def increment_statistic(self, row):
        row.play_count += 1
        row.last_played = datetime.now()

    def update_statistic(self, cls, attrib, value):
        existing = cls.select(getattr(cls.q, attrib) == value.id)
        for ex in existing:
            print 'found existing', ex
            self.increment_statistic(ex)
            break
        else:
            print 'creating new', cls, attrib, value
            ex = cls(**{attrib: value})
            self.increment_statistic(ex)

    def stream_song(self, id):
        metadata = self.get_track(id)

        send_title = False
        if 'icy-metadata' in self.headers:
            send_title = True

        if metadata:
            self.update_statistic(TrackStatistics, 'track', metadata)
            self.update_statistic(AlbumStatistics, 'album', metadata.album)
            self.update_statistic(ArtistStatistics, 'artist', metadata.artist)
            self.update_statistic(GenreStatistics, 'genre', metadata.genre)
            #TODO(nikhil) Fix Hi there
            self.wfile.write("ICY 200 OK\r\n")
            self.send_header("icy-notice1", "Hi there")
            self.send_header("icy-notice2", "Hi there")
            self.send_header("icy-name", "Muzicast")
            self.send_header("icy-genre", "Unknown")
            self.send_header("icy-url", "http://localhost:7664")
            self.send_header("icy-pub", "1")
# TODO(nikhil) decide all the ones below based on actual file
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("icy-br", metadata.bitrate)

            if send_title:
                self.send_header("icy-metaint", 512)

            self.wfile.write("\r\n")
            f = open(metadata.url.replace('file://', ''), 'rb')
            chunk = f.read(512)
            first = True
            try:
                while chunk:
                    self.connection.send(chunk)
#TODO(nikhil) deal with larger titles
                    if send_title:
                        if first:
                            title = "\x02StreamTitle='%s';StreamUrl='';"%metadata.title
                            title = title.ljust(33, '\x00')
                            self.connection.send(title)
                            first = False
                        else:
                            self.connection.send('\x00')
                    chunk = f.read(512)
            except socket.error:
                return
        else:
            self.send_error(404)

#TODO(nikhil) respect meta and send at bitrate

class StreamServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'New conn', addr
            handler = StreamJob(sock, addr, self)

server = StreamServer('0.0.0.0', 7665)
asyncore.loop()

#def stream(a, b):
#    print a, b
#    print a.recv(1024)
#    a.send("ICY 200 OK\r\n")
#    a.send("icy-name: Awesome\r\n")
#    a.send("icy-genre: Ambient\r\n")
#    a.send("Content-Type: audio/mpeg\r\n")
#    a.send("icy-br: 56\r\n")
#    a.send("\r\n")
#    size = os.stat("/shared/music/Harry Potter and the Deathly Hallows Part I/01 The Oblivation.mp3").st_size
#    f = open("/shared/music/Harry Potter and the Deathly Hallows Part I/01 The Oblivation.mp3", 'rb')
#    chunk = f.read(512)
#    while chunk:
#        a.send(chunk)
#        chunk = f.read(512)
#    a.close()
#
#def shutdown():
#    print "Shut down"
#
