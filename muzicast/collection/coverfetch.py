import sys
from hashlib import md5
import urllib
import Image
import cStringIO

import pylast

API_key = "d4e4bcc1745369ea3319820b31f3f637"
API_secret = "397a9d0662394ee5aff40bc9beeb4882"

def fetch_cover(artist, album, save_url):
    """
    Tries to fetch an album cover for track `url`
    from Last.FM and save it to `save_url`

    Returns save_url on success, None on failure.
    """

    connection = pylast.LastFMNetwork(api_key = API_key,api_secret = API_secret)
    album = connection.get_album(artist, album)
    image = album.get_cover_image()
    print 'got image', image

    if not image:
    	return None

    try:
        req = urllib.urlopen(image)
        im = cStringIO.StringIO(req.read())
        img = Image.open(im)
        print 'got image', img

        img.save(save_url)
        print 'saved image'
        return save_url
    except (IOError, IndexError):
        print 'got exception'
        return None

if __name__ == '__main__':
	print fetch_cover(sys.argv[1], '/tmp/test.png')
