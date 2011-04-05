import asyncore
import BaseHTTPServer
import os
import math
import sys
import signal
import socket
from datetime import datetime
import time
import sqlobject
import struct
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
            self.increment_statistic(ex)
            # IMPORTANT: This break
            # SHOULD NOT be removed
            # In Python the else clause is executed
            # only if the loop exits without hitting a break.
            # When an entry is found we don't want to create
            # a new one
            break
        else:
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
            self.wfile.write("ICY 200 OK\r\n")
            self.send_header("icy-notice1", "Welcome to a Muzicast streaming server")
            self.send_header("icy-notice2", "Register to be able to save playlists.")
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
                    if send_title:
                        if first:
                            # In Shoutcast, a byte is sent
                            # identifying the size of the following
                            # meta-data in multiples of 16
                            # So if the byte is 4, 64 bytes of data follows.
                            # Here we first get the length of the title
                            # in chunks of 16, then generate a format string
                            # for the 'struct' module with the right
                            # count inserted before the string packing instruction
                            # so that the title is padded with null bytes.
                            title = "StreamTitle='%s';StreamUrl='';"%metadata.title
                            length = math.ceil(len(title)/16.0)
                            fmt = "B%ds"%(length*16)
                            self.connection.send(struct.pack(fmt, length, str(title)))
                            first = False
                        else:
                            self.connection.send('\x00')
                    chunk = f.read(512)
            except socket.error:
                return
        else:
            self.send_error(404)

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
