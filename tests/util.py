import sys, os, string
sys.path.insert(0, os.path.abspath('.'))
letters = bytes(string.ascii_letters, 'ascii')

def basic_test_c(c, d):
    res = b''
    for b in letters:
        res += c.compress(bytes([b]))
    res += c.flush()
    assert d(res) == letters

def basic_test_d(d, c):
    res = b''
    for b in c(bytes(letters)):
        res += d.decompress(bytes([b]))
    assert res == letters
    assert not d.unused_data
