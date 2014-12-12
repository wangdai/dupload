import os
import hashlib

from .config import CAT_KEYS, CATEGORY, HASH_SIZE, OBS_ENC

def splitext(path):
    root, ext = os.path.splitext(path)
    if ext in ('.gz', '.bz2', '.xz'):
        root, ext_pre = os.path.splitext(root)
        ext = ext_pre + ext
    return (root, ext)

def judgecat(ext):
    for key in CAT_KEYS:
        if ext in CATEGORY.get(key):
            return key
    return 'other'

def filesize(f):
    oldpos = f.tell()
    size = f.seek(0, os.SEEK_END)
    f.seek(oldpos)
    return size

def filemd5(f):
    oldpos = f.tell()
    fb_arr = f.read(HASH_SIZE)
    f.seek(oldpos)
    return hashlib.md5(fb_arr).hexdigest()

def obfuscate(v):
    v = OBS_ENC['pace'] * v + OBS_ENC['offset']
    cl = []
    radix = len(OBS_ENC['str'])
    while v > 0:
        v, mod = divmod(v, radix)
        cl.insert(0, OBS_ENC['str'][mod])
    s = ''.join(cl)[::-1]
    h = hashlib.sha1(s.encode()).hexdigest()
    m = []
    for i in range(1, 5):
        c = h[-i]
        if ord(h[i]) % 2 == 0:
            m.append(c.lower())
        else:
            m.append(c.upper())
    return ''.join(m[:2]) + s + ''.join(m[-2:])

def clarify(s):
    s = s[2:-2]
    s = s[::-1]
    cl = list(OBS_ENC['str'])
    radix = len(OBS_ENC['str'])
    v = 0
    for c in s:
        v = radix * v + cl.index(c)
    v = (v - OBS_ENC['offset']) // OBS_ENC['pace']
    return v

