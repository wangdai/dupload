import hashlib

from sqlalchemy import desc

import config
import utils
from models import Item

def get_items(session, offset, limit, cat=None):
    offset = 0 if offset < 0 else offset
    limit = 0 if limit < 0 else limit
    if cat not in config.CAT_KEYS:
        return session.query(Item) \
                .order_by(desc(Item.lastmodified))[offset:offset+limit]
    else:
        return session.query(Item).filter_by(cat=cat) \
                .order_by(desc(Item.lastmodified))[offset:offset+limit]

def get_items_count(session, cat=None):
    if cat not in config.CAT_KEYS:
        return session.query(Item).count()
    else:
        return session.query(Item).filter_by(cat=cat).count()

def create_item(session, file, name, desc):
    root, ext = utils.splitext(name)
    # TODO handle cat is None
    cat = utils.judgecat(ext)
    # TODO check file is None
    # check file size
    file.seek(0)
    fb_arr = file.read(config.HASH_SIZE)
    file.seek(0)
    size = len(fb_arr)
    hashvalue = hashlib.md5(fb_arr).hexdigest()
    if exists(session, hashvalue):
        # TODO
        pass
    hashname = hashvalue + ext
    item = Item(name, hashname, size, cat, desc)
    session.add(item)
    return item

def exists(session, hashvalue):
    item = session.query(Item).filter(Item.hashname.like(hashvalue+'%')).first()
    if item is None:
        return False
    return True

