import sys
import os
import stat
import tempfile

from nose.tools import *

from muzicast.web import app
from muzicast.web.util import make_pls_playlist

class FakeTrack(object):
    def __init__(self, id):
        self.id = id

class TestPls(object):
    def setUp(self):
        self.app = app.test_client()
        for i in range(1, 11):
            self.app.get('/track/add/%d'%i)
        self.pls = self.app.get('/playlist/download/playlist.pls').data

    def test_pls_header(self):
        assert self.pls.split()[0] == '[playlist]'

    def test_count(self):
        assert self.pls.count('Title') == 10

    def test_version(self):
        assert self.pls.split()[-1] == 'Version=2'
