import os

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
    return None

