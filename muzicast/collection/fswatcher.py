from watchdog.events import FileSystemEventHandler

from muzicast.meta import Track

class CollectionEventHandler(FileSystemEventHandler):
    def __init__(self, scanner):
        FileSystemEventHandler.__init__(self)
        self.scanner = scanner

    def on_moved(self, event):
# a move is simple to handle, search for track
# with src and modify it to dest
# TODO(nikhil) handle directory move
        print event.src_path, '->', event.dest_path
        entries = list(Track.selectBy(url='file://' + event.src_path))
        if entries:
            for entry in entries:
            	print entry

    def on_created(self, event):
        print "Created", dir(event), event.src_path

    def on_deleted(self, event):
        print "Deleted", dir(event), event.src_path

    def on_modified(self, event):
        print "Modified", dir(event), event.src_path

