# -*- coding: utf-8 -*-
# Constants used in various parts of QL, mostly strings.

import os
import locale

VERSION_TUPLE = (0, 1, 0)
VERSION = ".".join(map(str, VERSION_TUPLE))

HOME    = os.path.expanduser(u"~")
if 'MUZICAST_USERDIR' in os.environ:
    USERDIR = os.environ['MUZICAST_USERDIR']
else:
    USERDIR = os.path.join(HOME, ".muzicast")

CONFIG = os.path.join(USERDIR, "config")
DB_FILE = os.path.join(USERDIR, "collection.db")
BASEDIR = os.path.dirname(os.path.realpath(__file__))

AUTHORS = sorted("""\
TODO
""".strip().split("\n"))

try: ENCODING = locale.getpreferredencoding()
except locale.Error: ENCODING = "utf-8"

FSCODING = "utf-8"

del(os)
del(locale)

