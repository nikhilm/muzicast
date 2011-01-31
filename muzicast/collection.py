import os
import sqlite3
import mutagen
import logging
from watchdog.events import FileSystemEventHandler

import gevent
from gevent.pool import Pool

def update_job(url):
    """ Scan a file.

    """
    
    
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
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.DEBUG)
        self.directories = list_of_directories

    def update(self, url):
        self.log.debug("Updating %s", url)
        gevent.sleep(0.5)

    def requires_update(self):
        return False

    def full_scan(self):
        # incremental scan with require_update always true
        old_requires_update = self.requires_update
        self.requires_update = lambda x: True
        self.incremental_scan()
        self.requires_update = old_requires_update

    def incremental_scan(self):
        job_pool = Pool(10)

        for directory in self.directories:
            for dirpath, dirnames, filenames in os.walk(directory):
                # only get the directories we know are modified
                # this way os.walk is more efficient
                [dirnames.remove(dir) for dir in dirnames if not self.requires_update(os.path.join(dirpath, dir))]
                
                self.log.debug("Directory %s Scanning %s", dirpath, dirnames)

                for file in filenames:
                    fn = os.path.join(dirpath, file)
                    if self.requires_update(fn):
                        # TODO: Do we wait around for updates to occur
                        # or do we have a two step pool
                    	job_pool.spawn(self.update, fn)
