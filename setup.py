from distutils.core import setup
import glob
import py2exe

setup(name='Muzicast',
      version='1.0',
      description='Music Streaming Server',
      author='Nikhil Marathe',
      author_email='nsm.nikhil@gmail.com',
      url='http://github.com/nikhilm/muzicast/',
      packages=['muzicast', 'muzicast.web', 'muzicast.collection', 'muzicast.collection.formats', 'muzicast.collection.util'],
      modules=['muzicast.web.principal', 'muzicast.streamer'],
      console=['run.py'],
      package_data={'muzicast.web': ['templates/master.html']},
      install_requires=['Flask>=0.6', 'watchdog>=0.5', 'sqlobject', 'jinja2', 'blinker', 'pylast'],
      options= {'py2exe': {
                        'skip_archive': True,
                        'bundle_files': 3,
                        'packages': ['werkzeug', 'jinja2', 'sqlobject', 'blinker', 'Image', 'pylast', 'muzicast.collection.formats', 'watchdog', 'pathtools', 'brownie'],
                        'excludes': ['tcl']
                    }},
      data_files=[
        ('templates', glob.glob('muzicast/web/templates/*.html')),
        ('templates/admin',glob.glob('muzicast/web/admin/*.html'))
      ]
     )
