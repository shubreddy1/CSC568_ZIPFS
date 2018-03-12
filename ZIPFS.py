#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time
import zipfile
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
## Used memory.py from the official fusepy git source as the base to build the program
if not hasattr(__builtins__, 'bytes'):
    bytes = str

class Memory(LoggingMixIn, Operations):
    def __init__(self,filename):
	self.zf=zipfile.ZipFile(filename)
        self.files = {}
	self.gfiles = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()
	self.gfiles['/'] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2)
	print("files in the zip file ",self.zf.namelist())
	for fname in self.zf.namelist():
		if fname[-1]=='/':
			self.gfiles['/'+fname[:-1]] = dict(
            		   st_mode=(S_IFDIR | 1),
            		   st_nlink=2,
            		   st_size=self.calc('/'+fname),
            		   st_ctime=time(),
            		   st_mtime=time(),
            		   st_atime=time())
        		self.gfiles['/'+fname[:-1]]['st_nlink'] += 1
		else:
			self.gfiles['/'+fname] = dict(
	            	    st_mode=33204L,
	            	    st_nlink=1,
	            	    st_size=len(self.zf.read(fname)),
	            	    st_ctime=time(),
	            	    st_mtime=time(),
	            	    st_atime=time())
			self.fd+=1
	self.uPath("/")
	print("self files ",self.files)


    def calc(self,dpath):
	print("calculating ",dpath)
	if dpath[-1]!='/':
		return len(self.zf.getinfo(dpath[1:]).compress_size)
	total=0
	for x in self.zf.namelist():
		tname='/'+x
		if tname.startswith(dpath) and len(tname)!=len(dpath):
			total+=len(self.zf.read(x))
	return total


    def uPath(self,cpath):
	if cpath[-1]!="/":
		cpath+='/'
	print("calling update on ",cpath)
	print(self.gfiles.keys())
	l1=len(cpath)
	self.files={}
	now = time()
	self.files['/'] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2)
	nc=cpath.count('/')
	for fname in self.gfiles:
		if (fname.count('/')==nc and fname.startswith(cpath) and len(fname)>l1) or (fname.count('/')==nc+1 and fname[-1]=='/' and len(fname)>l1):
			print("filename ",fname)
			if fname[-1]=='/' and fname.count('/')==nc+1:
				self.files[fname[:-1]]=self.gfiles[fname]
			else:
				srev=fname[::-1]
				s_in=srev.find('/')
				act=srev[:s_in+1][::-1]
				print("actual filename ",act)
				self.files[act]=self.gfiles[fname]

    def create(self, path, mode):
	print("create called")
        self.files[path] = dict(
            st_mode=(S_IFREG | mode),
            st_nlink=1,
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time())

        self.fd += 1
        return self.fd

    def getattr(self, path, fh=None):
	print("getattr called  ",path,"   ",self.files)
        if path not in self.gfiles:
            raise FuseOSError(ENOENT)
	#print("ARR",arr)
	#self.uPath(self.path+path)
        return self.gfiles[path]

    def getxattr(self, path, name, position=0):
	print("getxattr called")
        attrs = self.files[path].get('attrs', {})
        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR

    def listxattr(self, path):
	print("listxattr called")
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()

    def mkdir(self, path, mode):
	print("mkdir called")
        print("Unsupported Function")

    def open(self, path, flags):
	print("open called")
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
	#print("actual files ",self.files)
	print("path ",path)
	print("read is being called ")
	print(path,size)
	fname=path[1:]
	print("content read is ",self.zf.read(fname))
        return self.zf.read(fname)

    def readdir(self, path, fh):
	print("\n\n\n READDIR called on ",path)
	#print("actual files",self.files)
	self.uPath(path)
	print("actual files 2 ",self.files)        
	return ['.', '..'] + [x[1:] for x in self.files if x != '/']

    def readlink(self, path):
	print("readlink called")
        return self.data[path]

    def statfs(self, path):
	print("statfs called")
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def create(self, path, mode):
	print("Unsupported Function")

    def rename(self, old, new):
	print("Unsupported Function")

    def rmdir(self, path):
	print("Unsupported Function")

    def truncate(self, path, length, fh=None):
	print("Unsupported Function")

    def write(self, path, data, offset, fh):
	print("Unsupported Function")

    def chmod(self, path, mode):
	print("Unsupported Function")

    def chown(self, path, uid, gid):
	print("Unsupported Function")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('Mount')
    parser.add_argument('Zip_File_Name')
    #print parser
    args = parser.parse_args()
    #print(args.Mount)
    logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(Memory(args.Zip_File_Name), args.Mount, foreground=True, allow_other=True)
