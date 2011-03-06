import sys
import stat
import os
import logging
import datetime

from muzicast.meta import Track, Album, Artist, Genre, Composer
from muzicast.collection.formats import MusicFile

logging.basicConfig(level=logging.DEBUG)

def bake(url):
    """ Scan a file.

    """
    f = MusicFile(url)

    def get_row(cls, **kwargs):
        """
        runs a query with kwargs on cls SQLObject
        subclasses and if a result is found
        returns it, otherwise returns a new object
        with attributes as kwargs.
        """
        res = list(cls.selectBy(**kwargs))
        if len(res) > 0:
            return res[0]
        return cls(**kwargs)

    if f:
        d = {}
        d['url'] = 'file://' + url
        d['artist'] = get_row(Artist, name=f.get('artist', ''))
        d['album'] = get_row(Album, name=f.get('album', ''), artistID=d['artist'], image='')
        d['genre'] = get_row(Genre, name=f.get('genre', ''))
        d['composer'] = get_row(Composer, name=f.get('composer', ''))
        d['year'] = int(f.get('date', '-1'))
        d['title'] = f.get('title', '')
        d['comment'] = f.get('comment', '')
        try:
            d['tracknumber'] = int(f.get('tracknumber', '0'))
        except ValueError:
            d['tracknumber'] = 0

        try:
            d['discnumber'] = int(f.get('discnumber', '0')) or 1
        except ValueError:
            d['discnumber'] = 0

        d['bitrate'] = int(f.get('~#bitrate', '0'))
        d['duration'] = int(f.get('~#length', '0'))
        d['filesize'] = int(f.get('~#filesize', '0'))
        #TODO(nikhil) get filetype
        d['filetype'] = os.path.splitext(url)[1]
        #TODO(nikhil) get bpm or trash column
        d['bpm'] = 0
        print 'timestamp', datetime.datetime.fromtimestamp(int(f.get('~#mtime', '0')) or time.time())
        d['createdate'] = d['modifydate'] = datetime.datetime.fromtimestamp(int(f.get('~#mtime', '0')) or time.time())
        print '1'
        return d

    return None

def update_meta(obj, attrs):
    obj.set(**attrs)

class ScanRunner(object):
    def __init__(self, directory, full=False, last_shutdown_time=0):
        self.log = logging.getLogger('scanrunner-%d'%os.getpid())
        self.log.addHandler(logging.StreamHandler())
        self.directory = directory
        self.full = full
        self.last_shutdown_time = last_shutdown_time

    def scan(self):
        self.log.debug("starting scan on %s. full? %s. comparing against %d", self.directory, self.full, self.last_shutdown_time)
        if self.full:
            self.full_scan()
        else:
            self.incremental_scan()
        return None

    def full_scan(self):
        # incremental scan with require_update always true
        old_requires_update = self.requires_update
        self.requires_update = lambda x: True
        self.log.debug("FULL SCAN")
        self.incremental_scan()
        self.requires_update = old_requires_update

    def incremental_scan(self):
        for dirpath, dirnames, filenames in os.walk(self.directory):
            # only get the directories we know are modified
            # this way os.walk is more efficient
            [dirnames.remove(dir) for dir in dirnames if not self.requires_update(os.path.join(dirpath, dir))]
            
            #self.log.debug("Directory %s Scanning %s", dirpath, dirnames)

            for file in filenames:
                fn = os.path.join(dirpath, file)
                if self.requires_update(fn):
                    self.log.debug("UPDATING %s", fn)
                    # TODO: Do we wait around for updates to occur
                    # or do we have a two step pool
                    self.update(fn)

    def update(self, url):
        self.log.debug('before bake %s', url)
        info = bake(url)
        self.log.debug('Got info %s', info)
        if not info:
            return
        self.log.debug('after bake')
        # does it exist already?
        entry = list(Track.select(Track.q.url == ('file://'+url)))
        if entry:
            update_meta(entry[0], info)
        else:
            # insert new
            Track(**info)

    def requires_update(self, path):
        stat_info = os.stat(path)
        self.log.debug("Checking %s", path)
        if stat.S_ISDIR(stat_info.st_mode):
            self.log.debug("mtime for %s %d, lastshut %d", path, stat_info.st_mtime, self.last_shutdown_time)
            if stat_info.st_mtime > self.last_shutdown_time:
                return True
            return False

        # TODO(nikhil) handle various file cases
        return True

def start_scanrunner(*args):
    r = ScanRunner(*args)
    r.scan()
