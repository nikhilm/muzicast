import os
import sqlite3
import logging
import datetime
import time
from watchdog.events import FileSystemEventHandler

from muzicast.collection.formats import MusicFile
from muzicast.meta import Artist, Album, Genre, Composer, Track

def update_job(url):
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
        d['createdate'] = d['modifydate'] = datetime.datetime.fromtimestamp(int(f.get('~#mtime', '0')) or time.time())

        #TODO(nikhil) select by ANDing all
        # then see if the filename is different
        # in which case we have to handle the
        # move operation. Otherwise insert a new
        # track
        existing_tracks = list(Track.selectBy(artist=d['artist'], album=d['album'], title=d['title']))
        if len(existing_tracks) > 0:
            most_likely = existing_tracks[0]
            #TODO(nikhil) handle move
        else:
            #TODO(nikhil) handle ascii encoding issues
            Track(**d)
    
class CollectionEventHandler(FileSystemEventHandler):
    def __init__(self, scanner):
        self.scanner = scanner

    def on_created(self, event):
        pass

    def on_modified(self, event):
        pass

class CollectionScanner(object):
    def __init__(self, list_of_directories):
        self.log = logging.getLogger('collectionscanner')
        #self.log.addHandler(logging.StreamHandler())
        self.log.addHandler(logging.NullHandler())
        self.log.setLevel(logging.DEBUG)
        self.directories = list_of_directories

    def update(self, url):
        pass
        #self.log.debug("Updating %s", url)

    def requires_update(self):
        return False

    def full_scan(self):
        # incremental scan with require_update always true
        old_requires_update = self.requires_update
        self.requires_update = lambda x: True
        self.incremental_scan()
        self.requires_update = old_requires_update

    def incremental_scan(self):
        for directory in self.directories:
            for dirpath, dirnames, filenames in os.walk(directory):
                # only get the directories we know are modified
                # this way os.walk is more efficient
                [dirnames.remove(dir) for dir in dirnames if not self.requires_update(os.path.join(dirpath, dir))]
                
                #self.log.debug("Directory %s Scanning %s", dirpath, dirnames)

                for file in filenames:
                    fn = os.path.join(dirpath, file)
                    if self.requires_update(fn):
                        # TODO: Do we wait around for updates to occur
                        # or do we have a two step pool
                        update_job(fn)
