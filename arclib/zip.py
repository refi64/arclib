from . import AbstractAdvancedFile, AbstractMemberInfo
from zipfile import is_zipfile as test, ZipFile as _zfile, ZipInfo as _info
import os as _os, datetime as _datetime
from . import _rfile

class Info(AbstractMemberInfo):
    _module = 'zip'

    def __init__(self, info):
        self.info = info

    @property
    def filename(self): return self.info.filename
    @filename.setter
    def filename(self, value):
        self.info.filename = value

    @property
    def size(self): return self.info.file_size
    @size.setter
    def size(self, value):
        self.info.file_size = value

    @property
    def mtime(self): return _datetime.datetime(*self.info.date_time)
    @mtime.setter
    def mtime(self, value):
        self.info.date_time = tuple(value.timetuple()[:6])

class File(AbstractAdvancedFile):
    def __init__(self, zipfile):
        self.__zip = zipfile

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self.__zip.close()

    def info_for(self, member):
        return Info(self.__zip.getinfo(member))

    def all_info(self):
        return list(map(Info, self.__zip.infolist()))

    def members(self):
        return self.__zip.namelist()

    def dump(self):
        self.__zip.printdir()

    def add(self, path, arcname=None, recursive=True):
        if _os.path.isdir(path) and recursive:
            for root, dirs, files in _os.walk(path):
                subroot = root[len(path):]

                for fpath in files:
                    fullpath = _os.path.join(root, fpath)
                    destpath = fullpath[len(path):].lstrip('/')

                    if arcname:
                        destpath = _os.path.join(arcname, destpath)

                    self.__zip.write(fullpath, destpath)
        else:
            self.__zip.write(path, arcname)

    def add_data(self, path, data):
        self.__zip.writestr(path, data)

    def extract(self, member, path=None, *, pwd=None):
        self.__zip.extract(member, path, pwd)

    def extract_all(self, path=None, members=None, *, pwd=None):
        self.__zip.extractall(path, members, pwd=pwd)

    def open(self, member, universal_newlines=False, *, pwd=None):
        try:
            fp = self.__zip.open(member, pwd=pwd)
        except KeyError:
            return None

        if universal_newlines:
            return _rfile.RTextFile(member, fp)
        else:
            return _rfile.RFile(member, fp)

def open(*args, **kw):
    return File(_zfile(*args, **kw))

def openobj(fileobj, **kw):
    return File(_zfile(fileobj, **kw))
