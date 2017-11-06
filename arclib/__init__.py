from abc import ABCMeta as _ABCMeta, abstractmethod as _abstractmethod
from functools import wraps as _wraps

def _uabstractmethod(f):
    @_wraps(f)
    def func(*args): raise NotImplementedError()
    return _abstractmethod(func)

class AbstractBasicCompressor(metaclass=_ABCMeta):
    @_uabstractmethod
    def compress(self, data): pass

    @_uabstractmethod
    def flush(): pass

class AbstractBasicDecompressor(metaclass=_ABCMeta):
    @_uabstractmethod
    def decompress(self, data): pass

    @property
    @_uabstractmethod
    def eof(self): pass

    @property
    @_uabstractmethod
    def unused_data(self): pass

class AbstractMemberInfo(metaclass=_ABCMeta):
    @property
    @_uabstractmethod
    def filename(self): pass

    @property
    @_uabstractmethod
    def size(self): pass

    @property
    @_uabstractmethod
    def mtime(self): pass

    # Yes, I am putting an implementation detail in an abstract class. No, I do
    # not care.
    def __str__(self):
        return '{}.{}({!r}, {}, {})'.format(self._module, self.__class__.__name__,
                                            self.filename, self.size, self.mtime)

    def __repr__(self): return str(self)

class AbstractAdvancedFile(metaclass=_ABCMeta):
    @_uabstractmethod
    def close(self): pass

    @_uabstractmethod
    def info_for(self, member): pass

    @_uabstractmethod
    def all_info(self): pass

    @_uabstractmethod
    def members(self): pass

    @_uabstractmethod
    def dump(self): pass

    @_uabstractmethod
    def add(self, path, arcname=None, *, recursive=True): pass

    @_uabstractmethod
    def add_data(self, path, data): pass

    @_uabstractmethod
    def extract(self, path=None, **kw): pass

    @_uabstractmethod
    def extract_all(self, path=None, members=None, **kw): pass

    @_uabstractmethod
    def open(self, member, universal_newlines=False, **kw): pass
