from UserDict import UserDict
import os

from muzicast import const

try:
    import simplejson as json
except ImportError:
    import json

class Config(UserDict):
    def __init__(self, fp=None):
        """
        Creates a JSON backed configuration object.

        If a file is passed,
        tries to load the file on initalization if it exists.

        Use it pythonically and call save
        when you are done.
        """
        UserDict.__init__(self)
        if fp:
            self.data = json.load(fp)

    def save(self, fp):
        """
        Saves the JSON object to file `fp`.

        `fp` should be opened in truncate mode.
        """
        json.dump(self.data, fp, indent=4)

class GlobalConfig(Config):
    def __init__(self):
        self.ensure_existence()
        try:
            f = open(const.CONFIG, 'r')
            Config.__init__(self, f)
            f.close()
        except IOError:
            Config.__init__(self, None)

    def save(self):
        self.ensure_existence()
        f = open(const.CONFIG, 'w+b')
        Config.save(self, f)
        f.close()

    def ensure_existence(self):
        if not os.path.exists(const.CONFIG):
        	if not os.path.exists(const.USERDIR):
        		os.mkdir(const.USERDIR)
