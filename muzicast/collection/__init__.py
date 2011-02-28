import os
import sqlite3
import logging
from watchdog.events import FileSystemEventHandler

from muzicast.collection.formats import MusicFile

def update_job(url):
    """ Scan a file.

    """
    f = MusicFile(url)
    
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
