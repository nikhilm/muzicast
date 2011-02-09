import os

from muzicast import const

def is_first_run():
    return not os.path.exists(const.CONFIG)
