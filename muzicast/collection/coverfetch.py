import sys
from hashlib import md5
import urllib
import Image
import cStringIO
import socket
from threading import Timer

import pylast

API_key = "d4e4bcc1745369ea3319820b31f3f637"
API_secret = "397a9d0662394ee5aff40bc9beeb4882"

socket.setdefaulttimeout(10)

def fetch_cover(artist, album, save_url):
    """
    Tries to fetch an album cover for track `url`
    from Last.FM and save it to `save_url`

    Returns save_url on success, None on failure.
    """

    connection = None
    try:
        connection = pylast.LastFMNetwork(api_key = API_key,api_secret = API_secret)
    except pylast.NetworkError:
        return None

    album_obj = None
    try:
        album_obj = connection.get_album(artist, album)
    except pylast.NetworkError:
        return None

    image = None
    try:
        image = album_obj.get_cover_image()
    except (pylast.NetworkError, pylast.WSError, pylast.MalformedResponseError):
        return None

    if not image:
    	return None

    try:
        req = urllib.urlopen(image)
        def close(f):
            raise Exception()
            f.close()
	
        t = Timer(10, close, [req])
        t.start()
        im = cStringIO.StringIO(req.read())
        t.cancel()
        img = Image.open(im)

        img.save(save_url)
        return save_url
    except (IOError, IndexError), err:
        return None

if __name__ == '__main__':
	print fetch_cover(sys.argv[1], sys.argv[2], sys.argv[3])
