import sys
import stat
import os
import logging

logging.basicConfig(level=logging.DEBUG)

class ScanRunner(object):
    def __init__(self, directory, full=False, last_shutdown_time=0):
        self.log = logging.getLogger('scanrunner-%d'%os.getpid())
        self.log.addHandler(logging.StreamHandler())
        self.directory = directory
        self.last_shutdown_time = last_shutdown_time

        self.log.debug("starting scan on %s. full? %s. comparing against %d", directory, full, last_shutdown_time)
        if full:
        	self.full_scan()
        else:
        	self.incremental_scan()

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

    def update(self, url):
        pass
        #self.log.debug("Updating %s", url)

    def requires_update(self, path):
        stat_info = os.stat(path)
        if stat.S_ISDIR(stat_info.st_mode):
            if stat_info.st_mtime > self.last_shutdown_time:
            	return True
            return False

        # TODO(nikhil) handle various file cases
        return True
