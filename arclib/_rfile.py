import io

class RFile:
    def __init__(self, name, fp):
        self.__name = name
        self.__fp = fp

    @property
    def name(self): return self.__name

    def read(self, size=-1):
        return self.__fp.read(size)

class RTextFile(io.TextIOWrapper):
    def __init__(self, name, *args, **kw):
        self.__name = name
        super(RTextFile, self).__init__(*args, **kw)

    @property
    def name(self): return self.__name
