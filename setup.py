from distutils.core import setup

with open('README.rst') as f:
    descr = f.read()

setup(name='arclib',
      version='0.1',
      description="A unified API for accessing Python's compression formats",
      long_description=descr,
      author='Ryan Gonzalez',
      author_email='rymg19@gmail.com',
      url='https://github.com/kirbyfan64/arclib',
      packages=['arclib'],
      classifiers=[
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: System :: Archiving',
      ],
)
