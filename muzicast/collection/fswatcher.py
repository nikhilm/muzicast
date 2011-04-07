import os
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
        # a created event is always followed by a modify event
        # due to the actual data write that occurs to the file
        # unless its a zero-byte file in which case we don't want
        # to scan it anyway. So on_created does not do any handling
        # it is done by on_modified
        pass

    def on_deleted(self, event):
        # instead of bothering with file/directory changes
        # we simply match path and drop all tracks.
        tracks = Track.select(Track.q.url.startswith('file://'+event.src_path))
        [track.destroySelf() for track in tracks]


    def on_modified(self, event):
        print "Modified", dir(event), event.src_path
        if event.is_directory:
            self.scanner.scan_directory(event.src_path, False)
        else:
            self.scanner.scan_directory(os.path.dirname(event.src_path), False)
