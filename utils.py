import os

def splitext(path):
    root, ext = os.path.splitext(path)
    if ext in ('.gz', '.bz2', '.xz'):
        root, ext_pre = os.path.splitext(root)
        ext = ext_pre + ext
    return (root, ext)
