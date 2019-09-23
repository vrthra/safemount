import setuptools

setuptools.setup(
        name='safemount',
        version='0.1',
        author='Rahul Gopinath',
        author_email='rahul@gopinath.org',
        description='A FUSE mount that only permits safe characters in the file names',
        long_description='A FUSE mount that only permits safe characters in the file names',
        url='http://github.com/vrthra/safemount',
        packages=setuptools.find_packages(),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX",
            "Topic :: System :: Filesystems",
            "Topic :: Security"
            ],
        )
