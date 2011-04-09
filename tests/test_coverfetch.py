import sys
import os
import stat
import tempfile

from nose.tools import *

from muzicast.collection.coverfetch import fetch_cover

def test_success():
    assert fetch_cover('Arcade Fire', 'Neon Bible', '/tmp/test-cover-1.png') == '/tmp/test-cover-1.png'

def test_bad_artist():
    assert fetch_cover('abcdefghijklmnopqrstuvwxyz', 'Neon Bible', '/tmp/test-cover-2.png') == None

def test_bad_album():
    assert fetch_cover('Arcade Fire', 'they have no album like this', '/tmp/test-cover-3.png') == None
