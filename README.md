# safemount

We have to jump through multiple hoops in shell scripts to ensure that our
scripts handle special characters such as space, hyphen etc. properly. A number
of security vulnerabilities exist because of mishandling of these characters.

However, these special characters, while important for GUI are not a necessity
for command line. The idea of this library is to provide a FUSE filesystem that
mounts a given directory under a mount point such that all the special
characters are URL encoded. We include `-` in the list of characters that are
encoded. Further, we also remove `.` and `..` from the directory listing.

With this, the shell scripts can assume that none of the directory
or file names contain special characters.

The usage is as follows:

```
python -m safemount ./mydir ./mntpoint
```

See also:
1. https://dwheeler.com/essays/filenames-in-shell.html
2. https://dwheeler.com/essays/fixing-unix-linux-filenames.html
3. https://lwn.net/Articles/325304/
4. https://lwn.net/Articles/686789/
