import sys
import os
import stat
import tempfile

from nose.tools import *

from muzicast.collection.coverfetch import fetch_cover

def test_success():
    assert fetchcover('Arcade Fire', 'Neon Bible', '/tmp/test-cover-1.png') == 'test-cover-1.png'

def test_bad_artist():
    assert fetchcover('abcdefghijklmnopqrstuvwxyz', 'Neon Bible', '/tmp/test-cover-2.png') == None

def test_bad_album():
    assert fetchcover('Arcade Fire', 'they have no album like this', '/tmp/test-cover-3.png') == None
