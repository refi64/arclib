from util import *
from arclib import bz2
from bz2 import compress, decompress

def test_incremental_compress():
    basic_test_c(bz2.Compressor(), decompress)

def test_incremental_decompress():
    basic_test_d(bz2.Decompressor(), compress)
