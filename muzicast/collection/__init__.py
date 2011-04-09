import os
import sys
import sqlite3
import datetime
import time
import signal
from sqlobject.dberrors import OperationalError
from multiprocessing import Pool
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from muzicast.collection.fswatcher import CollectionEventHandler
from muzicast.collection.scanrunner import start_scanrunner
from muzicast.meta import *
from muzicast.config import GlobalConfig
from muzicast.const import CONFIG, USERDIR

class ConfigWatcher(FileSystemEventHandler):
    def __init__(self, scanner):
        FileSystemEventHandler.__init__(self)
        self.scanner = scanner

    def on_modified(self, event):
        if event.src_path == CONFIG:
            self.scanner.configuration_changed()
    
class CollectionScanner(object):
    def __init__(self):

        self.fswatcher = CollectionEventHandler(self)
        self.observer = Observer()
        self.watches = {}
        self.scanner_pool = Pool(processes=4)

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)

    def scan_directory(self, directory, full_scan):
        self.scanner_pool.apply_async(start_scanrunner, [directory, full_scan, self.last_shutdown_time])

    def add_directory(self, directory, full_scan=False):
        # start a full scan if required
        # otherwise do an incremental
        # and schedule a watch.

        self.scan_directory(directory, full_scan)
        #start_scanrunner(directory, full_scan, self.last_shutdown_time)
        #TODO(nikhil) fix me
        self.watches[directory] = True
        self.watches[directory] = self.observer.schedule(self.fswatcher, path=directory, recursive=True)

    def remove_directory(self, directory):
        try:
            self.observer.unschedule(self.watches[directory])
            del self.watches[directory]
        except KeyError:
            pass
        # also remove all tracks within that directory from DB
        tracks = Track.select(Track.q.url.startswith('file://'+directory))
        for track in tracks:
            track.destroySelf()

    def configuration_changed(self):
        # check if collection dirs have
        # been changed since we last started
        # if yes, we will do a full rescan
        # otherwise, an incremental scan.

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

        full_scan = False
        if last_scan < paths_saved_at:
            full_scan = True

        if full_scan:
            try:
                # for a full scan, first wipe all tables
                Artist.deleteMany(None)
                Album.deleteMany(None)
                Genre.deleteMany(None)
                Composer.deleteMany(None)
                Track.deleteMany(None)
                TrackStatistics.deleteMany(None)
                AlbumStatistics.deleteMany(None)
                ArtistStatistics.deleteMany(None)
                GenreStatistics.deleteMany(None)
            except OperationalError:
                pass

        # first remove watches on
        # any directories that have been
        # removed from the collection directories
        existing_directories = set(self.watches.keys())
        for dir in existing_directories.difference(collection_directories):
            self.remove_directory(dir)

        for dir in collection_directories:
            if dir in self.watches:
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
        self.scanner_pool.terminate()

        self.observer.join()
        self.scanner_pool.join()
        sys.exit(0)

if __name__ == '__main__':
    c = CollectionScanner()
    c.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        c.quit()
