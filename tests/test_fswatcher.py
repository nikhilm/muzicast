import sys
import os
import stat
import tempfile
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from nose.tools import *

from muzicast.collection.fswatcher import CollectionEventHandler

class FakeScanner(object):
    def __init__(self):
        self.count = 0

    def scan_directory(self, dir, full):
        self.count += 1
        

def create_watcher():
    obs = Observer()
    scanner = FakeScanner()
    fswatcher = CollectionEventHandler(scanner)
    return (obs, fswatcher, scanner)

def test_file_create():
    direc =  tempfile.mkdtemp()
    ob, watcher, scanner = create_watcher()
    ob.schedule(watcher, path=direc, recursive=True)
    ob.start()
        
    time.sleep(1)
    f = open(os.path.join(direc, "music"), 'w')
    f.write('test\n')
    f.close()
    time.sleep(1)
    assert scanner.count == 1
    ob.stop()
    shutil.rmtree(direc)

def test_file_modification():
    direc =  tempfile.mkdtemp()
    with tempfile.NamedTemporaryFile(dir=direc) as file:
        ob, watcher, scanner = create_watcher()
        ob.schedule(watcher, path=direc, recursive=True)
        ob.start()
        
        time.sleep(1)
        os.utime(file.name, None)
        time.sleep(1)
        ob.stop()
        assert scanner.count == 1
    shutil.rmtree(direc)

def test_file_delete():
    direc =  tempfile.mkdtemp()
    fd, f = tempfile.mkstemp(dir=direc)
    os.utime(f, None)

    ob, watcher, scanner = create_watcher()
    ob.schedule(watcher, path=direc, recursive=True)
    ob.start()
    
    time.sleep(1)
    os.remove(f)
    time.sleep(1)
    ob.stop()
    assert scanner.count == 0
    shutil.rmtree(direc)
