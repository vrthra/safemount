import setuptools
with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
        name='safemount',
        version='0.6',
        author='Rahul Gopinath',
        author_email='rahul@gopinath.org',
        description='A FUSE mount that only permits safe characters in the file names',
        long_description=long_description,
        url='http://github.com/vrthra/safemount',
        packages=['safemount'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX",
            "Topic :: System :: Filesystems",
            "Topic :: Security"
            ],
        )
