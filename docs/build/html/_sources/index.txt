arclib
======

Python has a very thorough standard library, including a variety of modules for
compressing and decompressing data. However, all of them have different APIs for
working with them., leading to difficulty in attempting to support multiple
archive formats. arclib is an attempt to fix this by providing a common API that
bridges the various archive modules in Python.

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
   
   Returns a ``File`` with the given arguments. Each module's ``open`` function
   is an alias for it's corresponding Python module's ``open`` and therefore
   returns the module's ``File``. For instance, ``arclib.gz.open`` is an alias
   for Python's own ``gzip.open`` and returns ``gzip.GzipFile``.

Basic, one-shot
^^^^^^^^^^^^^^^

All the "basic" modules (gz, bz2, and lzma) implement this API:

detach, truncate
https://docs.python.org/3/library/io.html#io.BufferedIOBase

.. py:function:: compress(data)
   
   Compresses data using the corresponding compression method.
   
   :param bytes data: The data to compress.
   :returns bytes: The compressed data.

.. py:function:: decompress(data)
   
   Decompresses data using the corresponding decompression method.
   
   :param bytes data: The data to decompress.
   :returns bytes: The decompressed data.

In addition, their ``open`` function is the same as the base API.

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
      :returns bytes: A portion of compressed data, or an empty byte string. Note
                      that this data is **not** considered valid on its own, and
                      must be combined with both other calls to ``compress`` and
                      the result of :py:method:flush.
      
   
   .. py:method:: flush()
      
      Flushes the compressor's internal buffers.
      
      :returns bytes: The rest of the compressed data.

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
      :returns bytes: A portion of decompressed data, or an empty byte string.
                      Note that this data is **not** the complete decompressed
                      data, and must be combined with other calls to
                      ``decompress``.
   
   .. py:attribute:: eof
      
      Whether or not the end of the compressed data has been reached.
   
   .. py:attribute:: unused_data
      
      Any unused data left over after the decompression completed.
