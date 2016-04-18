from . import AbstractBasicCompressor, AbstractBasicDecompressor
from lzma import LZMACompressor as Compressor, LZMADecompressor as Decompressor,\
                 LZMAFile as File, open

AbstractBasicCompressor.register(Compressor)
AbstractBasicDecompressor.register(Decompressor)
