import sys
import stat
import os
import logging
import datetime
import hashlib

from muzicast.const import COVERSDIR
from muzicast.meta import Track, Album, Artist, Genre, Composer
from muzicast.collection.coverfetch import fetch_cover
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
        d['album'] = get_row(Album, name=f.get('album', ''), artistID=d['artist'])
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
        d['createdate'] = d['modifydate'] = datetime.datetime.fromtimestamp(int(f.get('~#mtime', '0')) or time.time())
        return d

    return None

def find_existing(url, attrs):
    #TODO: improve
    return list(Track.select(Track.q.url == ('file://'+url)))

def update_meta(obj, attrs):
    obj.set(**attrs)

def insert_meta(attrs):
    return Track(**attrs)

def set_album_cover(track_info):
    print 'Setting album cover for', track_info['album']
    if track_info['album'].image:
        # we already have a cover
        return track_info['album'].image

    if not os.path.exists(COVERSDIR):
        os.mkdir(COVERSDIR)

    filename = hashlib.sha1(track_info['album'].name).hexdigest() + '.png'
    path = os.path.join(COVERSDIR, filename)
    result = fetch_cover(track_info['artist'].name, track_info['album'].name, path)
    if not result:
        print 'none found'
        return None

    print 'found', path
    track_info['album'].image = path
    print 'returning'
    return path

class ScanRunner(object):
    def __init__(self, directory, full=False, last_shutdown_time=0):
        self.directory = directory
        self.full = full
        self.last_shutdown_time = last_shutdown_time

    def scan(self):
        if self.full:
            self.full_scan()
        else:
            self.incremental_scan()
        return None

    def full_scan(self):
        # incremental scan with require_update always true
        self.incremental_scan()

    def incremental_scan(self):
        for dirpath, dirnames, filenames in os.walk(self.directory):
            print dirpath, dirnames, filenames
            # only get the directories we know are modified
            # this way os.walk is more efficient
            remove = [x for x in dirnames if not self.requires_update(os.path.join(dirpath, x))]
            for entry in remove:
                dirnames.remove(entry)
            
            # at this point, modified directories are in dirnames
            # os.walk will take care of iterating over them
            # so we only iterate over files.
            for file in filenames:
                fn = os.path.join(dirpath, file)
                if self.requires_update(fn):
                    # TODO: Do we wait around for updates to occur
                    # or do we have a two step pool
                    self.update(fn)

    def update(self, url):
        info = bake(url)
        print 'info', info
        if not info:
            return
        set_album_cover(info)
        # does it exist already?
        entry = find_existing(url, info)
        # TODO:
        # also try that if the file was renamed
        # while muzicast was not running
        # then if the meta-data is an exact match
        if entry:
            update_meta(entry[0], info)
        else:
            # insert new
            insert_meta(info)

    def requires_update(self, path):
        if self.full: return True

        stat_info = os.stat(path)
        print "Checking %s", path
        if stat.S_ISDIR(stat_info.st_mode):
            print "mtime for %s %d, lastshut %d", path, stat_info.st_mtime, self.last_shutdown_time
            if stat_info.st_mtime > self.last_shutdown_time:
                return True
            return False

        # TODO(nikhil) handle various file cases
        return True

def start_scanrunner(*args):
    print "Launching scanrunner with", args
    r = ScanRunner(*args)
    r.scan()
