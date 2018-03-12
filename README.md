# CSC568_ZIPFS
Involves creating a read only file system by mounting a zip file to an empty directory (without extracting the contents of the file).
Implemented in Python (with zipfile library) using FusePy's memory.py as the base.
Supports cat, cp, ls, stat, find, file, less, grep (possibily du also).

Please type in the commands before executing the program

sudo wget https://github.com/terencehonles/fusepy/zipball/master

unzip master

cd terencehonles-fusepy-2da9212

sudo python setup.py install

cd ..

######################################################


Copy the program zipfs.py and ".zip" to a directory with an empty folder in it.

Excute using "sudo python zipfs.py mount_point zipfilename.zip"

Open another window/terminal to explore/traverse the mounted filesystem

To unmount use Ctrl+C or "sudo fusermount -u mountpoint"
