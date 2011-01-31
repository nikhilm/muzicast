import sys
print sys.path
from muzicast.collection import CollectionScanner

scanner = CollectionScanner(['/shared/music-test'])

assert type(scanner.directories) is list

scanner.full_scan()
