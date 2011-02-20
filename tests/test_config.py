import sys
import os
import stat
import tempfile

from nose.tools import *

from muzicast.config import Config, GlobalConfig

def test_config_empty_file():
    f = tempfile.TemporaryFile()
    assert_raises(ValueError, Config, f)

def test_config_no_file():
    c = Config()
    assert c.data == {}

def test_config_read_simple_file():
    handle = tempfile.TemporaryFile()
    handle.write('{ "spam": 5, "ham": 5.6, "array": [1, 2, 3] }')
    handle.flush()
    handle.seek(0)

    c = Config(handle)
    assert c['spam'] == c.data['spam'] == 5
    assert len(c['array']) == 3

def test_config_reload_simple_file():
    handle = tempfile.TemporaryFile()
    handle.write('{ "spam": 5, "ham": 5.6, "array": [1, 2, 3] }')
    handle.flush()
    handle.seek(0)

    c = Config(handle)
    c['spam'] += 1
    c['array'].append(42)

    handle.seek(0)
    c.save(handle)
    handle.seek(0)

    oc = Config(handle)
    assert oc['spam'] == 6
    assert len(oc['array']) == 4
    assert oc['array'][-1] == 42
