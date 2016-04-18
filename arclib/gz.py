from . import AbstractBasicCompressor, AbstractBasicDecompressor
from gzip import compress, decompress, GzipFile as File, open

class Compressor(AbstractBasicCompressor):
    __bufmax = 4096 # XXX: This isn't UINT_MAX!

    def __init__(self, compresslevel=9):
        self.__level = compresslevel
        self.__buffer = bytearray()
        self.__flushed = False

    def __noflush(self):
        if self.__flushed:
            raise ValueError('Compressor has been flushed')

    def compress(self, data):
        self.__noflush()
        compressed = compress(data)

        if len(self.__buffer)+len(compressed) > self.__bufmax:
            buffered, self.__buffer = bytes(self.__buffer), bytearray(compressed)
            return buffered
        else:
            self.__buffer.extend(compressed)
            return b''

    def flush(self):
        self.__noflush()
        self.__flushed = True
        return bytes(self.__buffer)

class Decompressor(AbstractBasicDecompressor):
    def __init__(self):
        self.__buffer = bytearray()

    def decompress(self, data):
        self.__buffer.extend(data)
        try:
            return decompress(self.__buffer)
        except (OSError, EOFError):
            return b''

    @property
    def eof(self): return False

    @property
    def unused_data(self): return b''
