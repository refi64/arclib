from util import *
from arclib import lzma
from lzma import compress, decompress

def test_incremental_compress():
    basic_test_c(lzma.Compressor(), decompress)

def test_incremental_decompress():
    basic_test_d(lzma.Decompressor(), compress)
