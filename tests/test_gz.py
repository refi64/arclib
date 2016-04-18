from util import *
from arclib import gz
from gzip import compress, decompress

def test_incremental_compress():
    basic_test_c(gz.Compressor(), decompress)

def test_incremental_decompress():
    basic_test_d(gz.Decompressor(), compress)
