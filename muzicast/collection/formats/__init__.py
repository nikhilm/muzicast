# Copyright 2004-2005 Joe Wreschnig, Michael Urman
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os
import sys

from glob import glob
from os.path import dirname, basename, join
from muzicast.collection import util

base = dirname(__file__)
self = basename(base)
parent = basename(dirname(base))
grandparent = basename(dirname(dirname(base)))
modules = [f[:-3] for f in glob(join(base, "[!_]*.py"))]
modules = ["%s.%s.%s.%s" % (grandparent, parent, self, basename(m)) for m in modules]

_infos = {}
for i, name in enumerate(modules):
    try: format = __import__(name, {}, {}, self)
    except Exception, err:
        continue
    format = __import__(name, {}, {}, self)
    for ext in format.extensions:
        _infos[ext] = format.info
    # Migrate pre-0.16 library, which was using an undocumented "feature".
    sys.modules[name.replace(".", "/")] = format
    if name and name.startswith("muzicast."):
        sys.modules[name.split(".", 1)[1]] = sys.modules[name]
    modules[i] = (format.extensions and name.split(".")[-1])

try: sys.modules["formats.flac"] = sys.modules["formats.xiph"]
except KeyError: pass
try: sys.modules["formats.oggvorbis"] = sys.modules["formats.xiph"]
except KeyError: pass

modules = filter(None, modules)
modules.sort()

def MusicFile(filename):
    for ext in _infos.keys():
        if filename.lower().endswith(ext):
            try:
                # The sys module docs say this is where the interactive
                # interpreter stores exceptions, so it should be safe for
                # us to do it -- if we're in the interpreter this does
                # nothing, and if we're not it lets us access them elsewhere.
                # WARNING: Not threadsafe. Don't add files from threads
                # other than the main one.
                sys.last_type = sys.last_value = sys.last_traceback = None
                return _infos[ext](filename)
            except:
                raise
                util.print_exc()
                lt, lv, tb = sys.exc_info()
                sys.last_type, sys.last_value, sys.last_traceback = lt, lv, tb
                return None
    else: return None

if sys.version_info < (2, 5):
    def supported(song):
        lower = song.key.lower()
        for ext in _infos.keys():
            if lower.endswith(ext):
                return True
        return False
else:
    extensions = tuple(_infos.keys())
    def supported(song):
        return song.key.lower().endswith(extensions)

#def filter(filename):
#    lower = filename.lower()
#    for ext in _infos.keys():
#        if lower.endswith(ext): return True
#    return False

from muzicast.collection.formats._audio import USEFUL_TAGS, MACHINE_TAGS, PEOPLE
