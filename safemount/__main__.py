import os
import os.path
from safemount.fs import init_fs

def print_help():
    print('''\
python -m safemount <root> <mountpoint>''')


def main(args):
    if len(args) < 3:
        return print_help()
    if not os.path.exists(args[1]):
        print("<root> %s does not exist" % args[1])
        exit(-1)
    if not os.path.isdir(args[1]):
        print("<root> %s is not a directory" % args[1])
        exit(-1)
    if not os.path.exists(args[2]):
        os.mkdir(args[2])
    if not os.path.isdir(args[2]):
        print("<mountpoint> %s is not a directory" % args[1])
        exit(-1)
    init_fs(args[1], args[2])

import sys
main(sys.argv)
