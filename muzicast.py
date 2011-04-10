#!/usr/bin/env python
import os
import time
import sys
import signal
import subprocess

dirpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirpath)
sys.path.append(os.path.join(dirpath, "3rdparty"))

if 'PYTHONPATH' in os.environ:
    os.environ['PYTHONPATH'] = os.pathsep.join(set(os.environ['PYTHONPATH'].split(os.pathsep) + sys.path))
else:
    os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)

from muzicast.const import BASEDIR, WEB_PORT, USERDIR
from muzicast.config import GlobalConfig
from muzicast.web import app

class Runner(object):
    def run(self):
        if not os.path.exists(USERDIR):
            os.mkdir(USERDIR)

        self.streamer = subprocess.Popen([sys.executable, os.path.join(BASEDIR, 'streamer.py')], env=os.environ)
        self.scanner = subprocess.Popen([sys.executable, os.path.join(BASEDIR, 'collection/__init__.py')], env=os.environ)
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        app.run('0.0.0.0', WEB_PORT, debug=False, use_reloader=False)

    def shutdown(self, signum, frame):
        self.streamer.terminate()
        self.scanner.terminate()
        config = GlobalConfig()
        config['last_shutdown_time'] = int(time.time())
        config.save()
        sys.exit(0)

if __name__ == '__main__':
    r = Runner()
    r.run()
