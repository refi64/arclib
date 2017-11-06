arclib
======

Python has a very thorough standard library, including a variety of modules for
compressing and decompressing data. However, all of them have different APIs for
working with them., leading to difficulty in attempting to support multiple
archive formats. arclib is an attempt to fix this by providing a common API that
bridges the various archive modules in Python.

Rationale
*********

A while back, I was trying to port a Python application from using zip files to
using tar files. To say it was "painful" is an understatement. The two modules
have conceptually similar but immensely different APIs. Therefore, I started work
on arclib to provide a unified API between the two, as well as between the other
archive modules in the standard library.

Archive categories
******************

``arclib`` divides Python's five archive modules (zipfile_, tarfile_, lzma_,
bzip2_, and gzip_) into three categories:

- Basic, one-shot: the only compression method in this category is gzip. With
  gzip, the only allowed method of compression and decompression is "one-shot",
  where all the data must be processed at once.

- Basic, incremental: LZMA and bzip2 fall under here. These not only allow
  one-shot but also incremental compression and decompression, where the data is
  fed in in small chunks.

- Complex, file-system: Tar and zip both are considering "complex" in arclib, in
  that they both allow one to store entire directory trees, not just chunks of
  data.

.. _zipfile: https://docs.python.org/3/library/zipfile.html
.. _tarfile: https://docs.python.org/3/library/tarfile.html
.. _lzma: https://docs.python.org/3/library/lzma.html
.. _bzip2: https://docs.python.org/3/library/bzip2.html
.. _gzip: https://docs.python.org/3/library/gzip.html

Modules
*******

arclib contains the following modules:

Basic compression/decompression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **arclib.gz:** A module that exposes a basic, one-shot gzip
  compression/decompression API.
- **arclib.bz2**: A module that exposes both a basic, one-shot bzip2
  compression/decompression and an incremental API.
- **arclib.lzma**: A module that exposes both a basic, one-shot LZMA
  compression/decompression and an incremental API.

**Note that arclib.gz does not expose an incremental API.**

Complex, file-system compression/decompression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both **arclib.zip** and **arclib.tar** expose an API that allows for manipulation
of their respective complex archive formats.

The APIs
********

Base
^^^^

All modules in arclib implement this API:

.. py:function:: open(*args, **kw)

   Returns a ``File`` with the given arguments.

Basic, one-shot
^^^^^^^^^^^^^^^

All the "basic" modules (gz, bz2, and lzma) implement this API:

detach, truncate
https://docs.python.org/3/library/io.html#io.BufferedIOBase

.. py:function:: compress(data)

   Compresses data using the corresponding compression method.

   :param bytes data: The data to compress.
   :return: The compressed data.
   :rtype: bytes

.. py:function:: decompress(data)

   Decompresses data using the corresponding decompression method.

   :param bytes data: The data to decompress.
   :return: The decompressed data.
   :rtype: bytes

In addition, their ``open`` function is an alias for the corresponding Python
module's ``open`` and therefore returns the module's ``File``. For instance,
``arclib.gz.open`` is an alias for Python's own ``gzip.open`` and returns
``gzip.GzipFile``.

Basic, incremental
^^^^^^^^^^^^^^^^^^

Both arclib.bz2 and arclib.lzma (***not*** arclib.gz) implement this API.

.. py:class:: Compressor

   A class that implements incremental compression. All types of this kind are
   instances of ``arclib.AbstractBasicCompressor``. Example usage:

   .. code-block:: python

      my_compressor = arclib.bz2.Compressor() # The compressor object.
      compressed_data = b'' # The resulting compressed data.
      compressed_data += my_compressor.compress(b'Something to compress...')
      compressed_data += my_compressor.compress(b'More stuff!')
      compressed_data += my_compressor.flush() # Always remember the flush call!

   .. py:method:: compress(data)

      Incrementally compresses data using the corresponding compression method.

      :param bytes data: The data to compress.
      :return: A portion of compressed data, or an empty byte string. Note that
               this data is **not** considered valid on its own, and must be
               combined with both other calls to ``compress`` and the result of
               :py:meth:`flush`.
      :rtype: bytes


   .. py:method:: flush()

      Flushes the compressor's internal buffers.

      :return: The rest of the compressed data.
      :rtype: bytes

.. py:class:: Decompressor

   A class that implements incremental compression. All types of this kind are
   instances of ``arclib.AbstractBasicDecompressor``. Example usage:

   .. code-block:: python

      compressed_data = arclib.bz2.compress(b'Some data to compress!')
      my_decompressor = arclib.bz2.Decompressor() # The decompressor object.
      decompressed_data = b'' # The resulting decompressed data.
      # Decompress some data.
      decompressed_data += my_decompressor.decompress(compressed_data[:5])
      # And some more data!
      decompressed_data += my_decompressor.decompress(compressed_data[5:])
      assert decompressed_data == b'Some data to compress!'
      assert my_decompressor.eof

   .. py:method:: decompress(data)

      Incrementally decompresses data using the corresponding decompression
      method.

      :param bytes data: The data to decompress.
      :return: A portion of decompressed data, or an empty byte string. Note that
               this data is **not** the complete decompressed  data, and must b
               combined with other calls to ``decompress``.
      :rtype: bytes

   .. py:attribute:: eof

      Whether or not the end of the compressed data has been reached.

   .. py:attribute:: unused_data

      Any unused data left over after the decompression completed.

Complex
^^^^^^^

Both arclib.zip and arclib.tar implement this API.

.. py:function:: open(*args, **kw)

   Opens an archive. All arguments are passed to the corresponding function; for
   instance, ``arclib.zip.open`` passes all its arguments to ``zipfile.open``.

   :return: The opened archive file.
   :rtype: :py:class:`File`

.. py:function:: openobj(fileobj, **kw)

   Opens the given file object. Whereas *open* opens a file path, *openobj* opens an
   in-memory file object.

   :return: The opened archive file.
   :rtype: :py:class:`File`

.. py:class:: File

   An opened archive file. Can be used as a context manager. Example:

   .. code-block:: python

      import arclib.zip

      with arclib.zip.open('myfile.zip') as f:
          # Stuff here.
      # f is automatically closed.

   .. py:method:: close()

      Close the archive file.

   .. py:method:: info_for(member)

      Returns an :py:class:`Info` object containing information about the given
      archive member.

      :param str member: A string describing the path to the archive member, e.g.
                         ``x/y/z``.
      :return: The member information object.
      :rtype: :py:class:`Info`

   .. py:method:: all_info()

      Retrieves :py:class:`Info` objects for all the archive's members.

      :return: A list of all the :py:class:`Info` objects for all the archive's
              members.
      :rtype: list of :py:class:`Info`

   .. py:method:: members()

      Retrieves all the archive's members.

      :return: A list of strings, one for each archive member.
      :rtype: list of str

   .. py:method:: dump()

      Dump a description archive's contents to standard output.

   .. py:method:: add(path, arcname=None, recursive=True)

      Adds a file or directory to the archive.

      :param str path: The path to add to the archive.
      :param str arcname: The name to give the file when placing it in the
                          archive. If ``None``, then it will be the same as
                          *path*, but with leading roots and the drive removed.
      :param bool recursive: If *path* is a directory and this is a truthy value,
                             then the directory's contents will also be added to
                             the archive.

   .. py:method:: add_data(path, data)

      Adds a ``bytes`` object to the archive.

      :param str path: The name to give the file when placing it in the archive.
      :param bytes data: The file's contents.

   .. py:method:: extract(member, path=None)

      Extracts a member from the archive.

      :param str member: The member to extract.
      :param str path: The target path to extract the member to; if ``None``, then
                       it will be the current directory.

      ``arclib.zip.File.extract`` also takes the following keyword argument:

      :param str pwd: The password to use to extract the file, or ``None``.

   .. py:method:: open(member, universal_newlines=False)

      Extracts a member from the archive into memory rather that onto the disk. Returns
      a bytes file-like object with the following properties:

      - *name* - The name of the member.
      - *read(size=-1)* - Read and return *size* bytes from the file.

      If ``universal_newlines`` is ``True``, then the file object will be an instance of
      ``io.TextIOWrapper`` that also has the ``name`` property.

      :param str member: The member to extract.
      :param str universal_newlines: If ``True``, returns an ``io.TextIOWrapper`` that
                                     also has a property *name*, which is the name of the
                                     member. Otherwise, returns a file-like object as
                                     mentioned above.

      ``arclib.zip.File.extract`` also takes the following keyword argument:

      :param str pwd: The password to use to extract the file, or ``None``.

.. py:class:: Info

   An object containing information about an archive member.

   .. py:attribute:: info

      The underlying, "true" info object. With ``arclib.zip.Info``, this is an
      instance of ``zipfile.ZipInfo``; with ``arclib.tar.Info``, this is an
      instance of ``tarfile.TarInfo``.

   .. py:attribute:: filename

      The name of the file within the archive.

   .. py:attribute:: size

      The number of bytes that the file takes up within the archive.

   .. py:attribute:: mtime

      A ``datetime.datetime`` object containing the last modification time of the
      file.
