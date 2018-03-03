# CSC568_ZIPFS
Involves creating a read only file system by mounting a zip file to an empty directory (without extracting the contents of the file).
Implemented in Python (with zipfile library) using FusePy's memory.py as the base.
Supports cat, cp, ls, stat, find, file, less, grep (possibily du also).
