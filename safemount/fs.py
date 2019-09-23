#!/usr/bin/env python

import os
import sys
import errno
import string
import pudb
bp = pudb.set_trace

from fuse import FUSE, FuseOSError, Operations

hex_values = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
}

DO_NOT_ENCODE='/_.+!(),' + string.ascii_letters + string.digits
VALID_CHARS = DO_NOT_ENCODE + '%'

def path_valid(s):
    for i in s:
        if i not in VALID_CHARS:
            raise FuseOSError(errno.EINVAL)

def path_encode(s):
    return ''.join([c if c in DO_NOT_ENCODE else "%%%02x" % ord(c) for c in s])

def path_decode(s):
    t = ''
    i = 0
    while i < len(s):
        c = s[i]
        if c == '%':
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values:
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t

class Passthrough(Operations):
    def __init__(self, root): self.root = root

    def _full_path(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(path_decode(full_path), mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(path_decode(full_path), mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(path_decode(full_path), uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(path_decode(full_path))
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path_ = self._full_path(path)
        full_path = path_decode(full_path_)

        #dirents = ['.', '..']
        # We disable '.' and '..' as it is not desirable in simple shell
        # scripts.
        dirents = []
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        entries = [path_encode(r) for r in dirents]
        return entries

    def readlink(self, path):
        full_path = self._full_path(path)
        pathname = os.readlink(path_decode(full_path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        path_valid(dev)
        return os.mknod(path_decode(self._full_path(path)), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(path_decode(full_path))

    def mkdir(self, path, mode):
        path_valid(path)
        return os.mkdir(path_decode(self._full_path(path)), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(path_decode(full_path))
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(path_decode(self._full_path(path)))

    def symlink(self, name, target):
        path_valid(target)
        return os.symlink(name, path_decode(self._full_path(target)))

    def rename(self, old, new):
        path_valid(new)
        return os.rename(path_decode(self._full_path(old)), path_decode(self._full_path(new)))

    def link(self, target, name):
        return os.link(path_decode(self._full_path(target)), path_decode(self._full_path(name)))

    def utimens(self, path, times=None):
        return os.utime(path_decode(self._full_path(path)), times)

    # File methods

    def open(self, path, flags):
        full_path = self._full_path(path)
        path_valid(full_path)
        return os.open(path_decode(full_path), flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        path_valid(full_path)
        return os.open(path_decode(full_path), os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(path_decode(full_path), 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def init_fs(root, mountpoint):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)

