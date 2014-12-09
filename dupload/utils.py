import os
import hashlib

import config

def splitext(path):
    root, ext = os.path.splitext(path)
    if ext in ('.gz', '.bz2', '.xz'):
        root, ext_pre = os.path.splitext(root)
        ext = ext_pre + ext
    return (root, ext)

def judgecat(ext):
    for key in config.CAT_KEYS:
        if ext in config.CATEGORY.get(key):
            return key
    return 'other'

def filesize(f):
    oldpos = f.tell()
    size = f.seek(0, os.SEEK_END)
    f.seek(oldpos)
    return size

def filemd5(f):
    oldpos = f.tell()
    fb_arr = file.read(config.HASH_SIZE)
    f.seek(oldpos)
    return hashlib.md5(fb_arr).hexdigest()

