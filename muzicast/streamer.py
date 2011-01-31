import os
import sys
import signal
import socket
import gevent
import time

from gevent.monkey import patch_all
from gevent.server import StreamServer
patch_all()

def stream(a, b):
    print a, b
    print a.recv(1024)
    a.send("ICY 200 OK\r\n")
    a.send("icy-name: Awesome\r\n")
    a.send("icy-genre: Ambient\r\n")
    a.send("Content-Type: audio/mpeg\r\n")
    a.send("icy-br: 56\r\n")
    a.send("\r\n")
    size = os.stat("/shared/music/Harry Potter and the Deathly Hallows Part I/01 The Oblivation.mp3").st_size
    f = open("/shared/music/Harry Potter and the Deathly Hallows Part I/01 The Oblivation.mp3", 'rb')
    chunk = f.read(512)
    while chunk:
    	a.send(chunk)
    	chunk = f.read(512)
    a.close()

server = gevent.server.StreamServer(('0.0.0.0', 4000), stream)

def shutdown():
    print "Shut down"

gevent.signal(signal.SIGINT, shutdown);

server.serve_forever()
