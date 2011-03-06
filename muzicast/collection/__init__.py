import os
import sys
import sqlite3
import logging
import datetime
import time
import signal
from multiprocessing import Pool
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from muzicast.collection.formats import MusicFile
from muzicast.collection.fswatcher import CollectionEventHandler
from muzicast.collection.scanrunner import ScanRunner
from muzicast.meta import Artist, Album, Genre, Composer, Track
from muzicast.config import GlobalConfig
from muzicast.const import CONFIG, USERDIR

logging.basicConfig(level=logging.DEBUG)

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

class ConfigWatcher(FileSystemEventHandler):
    def __init__(self, scanner):
        FileSystemEventHandler.__init__(self)
        self.scanner = scanner

    def on_modified(self, event):
        print "DETECTED CHANGE"
        if event.src_path == CONFIG:
            self.scanner.configuration_changed()
    
class CollectionScanner(object):
    def __init__(self, list_of_directories):
        self.log = logging.getLogger('collectionscanner')
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.DEBUG)

        self.directories = list_of_directories
        self.fswatcher = CollectionEventHandler(self)
        self.observer = Observer()
        self.watches = {}
        self.scanner_pool = Pool(processes=4)

        self.log.debug("Starting fswatcher")
#TODO(nikhil) enable this, but only after initialization (self.start) is done

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)
        self.start()

    def add_directory(self, directory, full_scan=False):
        # start a full scan if required
        # otherwise do an incremental
        # and schedule a watch.
        self.log.debug("Adding directory %s. full scan? %s", directory, full_scan)

        self.scanner_pool.apply_async(ScanRunner, [directory, full_scan, self.last_shutdown_time])
        #TODO(nikhil) fix me
        self.watches[directory] = True
        #self.watches[directory] = self.observer.schedule(self.fswatcher, path=directory, recursive=True)
        self.log.debug("Added watch, everything fine")

    def remove_directory(self, directory):
        try:
            self.log.debug("Removed watch on %s", directory)
            #TODO(nikhil) fixme
            #self.observer.unschedule(self.watches[directory])
            del self.watches[directory]
        except KeyError:
            self.log.debug("Could not unschedule %s", directory)

    def configuration_changed(self):
        # check if collection dirs have
        # been changed since we last started
        # if yes, we will do a full rescan
        # otherwise, an incremental scan.
        self.log.debug("Config changed")

        config = GlobalConfig()
        paths_saved_at = 0
        last_scan = 0
        self.last_shutdown_time = 0
        try:
            paths_saved_at = int(config['collection']['paths_saved_at'])
        except KeyError:
#TODO(nikhil) test this behaviour
            pass

        try:
            last_scan = int(config['collection']['last_scan'])
        except KeyError:
            last_scan = paths_saved_at - 1

        try:
            self.last_shutdown_time = int(config['last_shutdown_time'])
        except KeyError:
            pass

        collection_directories = set()
        try:
            collection_directories = set(config['collection']['paths'])
        except KeyError:
            pass
        self.log.debug("New collection paths %s", collection_directories)

        full_scan = False
        if last_scan < paths_saved_at:
            full_scan = True

        # first remove watches on
        # any directories that have been
        # removed from the collection directories
        existing_directories = set(self.watches.keys())
        self.log.debug("Existing %s", existing_directories)
        for dir in existing_directories.difference(collection_directories):
            self.remove_directory(dir)

        for dir in collection_directories:
            if dir in self.watches:
                self.log.debug("%s is already watched", dir)
                # directory is already being watched
                # do nothing
                pass
            else:
                self.add_directory(dir, full_scan)


    def start(self):
        self.configuration_changed()
        # Note: a 'first' scan is an
        # incremental scan behaving like a full
        # scan, so we don't have to explicitly
        # handle that case.
        # finally put a watch on the config file itself
        self.observer.schedule(ConfigWatcher(self), path=USERDIR)
        self.observer.start()

    def quit(self, signum, frame):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        # stop watching file before we make any changes
        self.observer.unschedule_all()
        self.observer.stop()
        # close all update threads
        # save current time
        config = GlobalConfig()
        try:
            config['collection']
        except KeyError:
            config['collection'] = {}
        now = int(time.time())
        config['collection']['last_scan'] = now
        config.save()

        self.scanner_pool.close()
        # wait a few seconds for finish
        time.sleep(3)
        self.scanner_pool.terminate()
        self.scanner_pool.join()
        sys.exit(0)

if __name__ == '__main__':
    config = GlobalConfig()

    # TODO(nikhil) needs to be refactored!
    if 'collection' in config and 'paths' in config['collection']:
        scanner = CollectionScanner(config['collection']['paths'])
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scanner.observer.stop()
        scanner.observer.join()
