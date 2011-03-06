import os
import time
import sys
import signal
import subprocess

from muzicast.const import BASEDIR, WEB_PORT
from muzicast.config import GlobalConfig
from muzicast.web import app

print 'Running', os.getpid(), os.getppid()

class Runner(object):
    def run(self):
        self.streamer = subprocess.Popen([sys.executable, os.path.join(BASEDIR, 'streamer.py')])
        self.scanner = subprocess.Popen([sys.executable, os.path.join(BASEDIR, 'collection/__init__.py')])
        print 'Started streamer PID %d'%self.streamer.pid
        print 'Started scanner PID %d'%self.scanner.pid
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        app.run('0.0.0.0', WEB_PORT, debug=True, use_reloader=False)
        #app.run('0.0.0.0', WEB_PORT, debug=False, use_reloader=False)

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
