from . import AbstractBasicCompressor, AbstractBasicDecompressor
from bz2 import BZ2Compressor as Compressor, BZ2Decompressor as Decompressor,\
                BZ2File as File, open

AbstractBasicCompressor.register(Compressor)
AbstractBasicDecompressor.register(Decompressor)
