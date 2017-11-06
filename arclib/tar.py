from . import AbstractAdvancedFile, AbstractMemberInfo
from tarfile import is_tarfile as test, TarFile as _tfile, TarInfo as _info
import datetime as _datetime, io as _io, time as _time
from . import _rfile

class Info(AbstractMemberInfo):
    _module = 'tar'

    def __init__(self, info, **kw):
        self.info = info

    @property
    def filename(self): return self.info.name
    @filename.setter
    def filename(self, value):
        self.info.name = value

    @property
    def size(self): return self.info.size
    @size.setter
    def size(self, value):
        self.info.size = value

    @property
    def mtime(self): return _datetime.datetime.fromtimestamp(self.info.mtime)
    @mtime.setter
    def mtime(self, value):
        self.info.mtime = value.timestamp()

class File(AbstractAdvancedFile):
    def __init__(self, tar):
        self.__tar = tar

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self.__tar.close()

    def info_for(self, member):
        return Info(self.__tar.getmember(member))

    def all_info(self):
        return list(map(Info, self.__tar.getmembers()))

    def members(self):
        return self.__tar.getnames()

    def dump(self):
        self.__tar.list()

    def add(self, path, arcname=None, *, recursive=True):
        self.__tar.add(path, arcname, recursive=recursive)

    def add_data(self, path, data):
        if isinstance(path, Info):
            info = path.info
        else:
            info = _info(path)
            info.size = len(data)
            info.mtime = _time.time()

        self.__tar.addfile(info, _io.BytesIO(data))

    def extract(self, member, path=None):
        self.__tar.extract(member, '' if path is None else path)

    def extract_all(self, path=None, members=None):
        self.__tar.extractall('.' if path is None else path, members)

    def open(self, member, universal_newlines=False):
        try:
            fp = self.__tar.extractfile(member)
        except KeyError:
            return None

        if universal_newlines:
            return _rfile.RTextFile(member, fp)
        else:
            return _rfile.RFile(member, fp)

def open(*args, **kw):
    return File(_tfile.open(*args, **kw))

def openobj(fileobj, **kw):
    return File(_tfile.open(name=kw.pop('name', None), fileobj=fileobj, **kw))
