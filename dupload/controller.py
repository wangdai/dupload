import hashlib
import json
import os

import bottle
from bottle import route, redirect, request, static_file
from bottle import jinja2_template as template
from bottle import jinja2_view as view
from sqlalchemy.orm import sessionmaker

from .config import PAGE_SIZE, CAT_KEYS, STATIC_PATH
from .service import get_items_count, get_items, create_item
from .models import engine, Item, ItemEncoder

Session = sessionmaker(bind=engine)

@route('/', method='GET')
def index():
    redirect('/items')

@route('/items', method='GET')
def items_get():
    session = Session()
    # current page
    p = request.query.p or 1
    p = int(p)
    offset = (p - 1) * PAGE_SIZE
    # category
    cat = request.query.cat
    cat = None if cat not in CAT_KEYS else cat
    rows = get_items_count(session, cat)
    # total pages
    tp = rows // PAGE_SIZE
    if rows % PAGE_SIZE != 0:
        tp += 1
    tp = 1 if tp <= 0 else tp
    # q = request.query.q
    param = dict()
    param['p'] = p
    param['tab'] = cat
    param['cats'] = sorted(CAT_KEYS)
    param['r'] = rows
    param['tp'] = tp
    param['items'] = get_items(session, offset, PAGE_SIZE, cat)
    session.close()
    return template('index', param)

@route('/items', method='POST')
def items_post():
    session = Session()
    try:
        upload = request.files.get('upload')
        desc = request.forms.get('description')
        size = request.forms.get('size')
        size = None if not size else int(size)

        item = create_item(session, upload.file, upload.raw_filename, size, desc)

        savepath = '%s/%s' % (STATIC_PATH, item.cat)
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        upload.file.seek(0)
        upload.filename = item.hashname
        upload.save(savepath)

        session.commit()
        return json.dumps(item, cls=ItemEncoder)
    except:
        session.rollback()
        raise
    finally:
        session.close()


@route('/items/<id>', method='DELETE')
def items_delete(id):
    session = Session()
    try:
        id = int(id)
        item = session.query(Item).filter_by(id=id).first()
        path = '%s/%s/%s' % (STATIC_PATH, item.cat, item.hashname)
        os.remove(path)
        session.delete(item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@route('/static/<path:path>', method='GET')
def static(path):
    return static_file(path, root=STATIC_PATH)

@route('/download/<path:path>', method='GET')
def download(path):
    f = request.query.f
    return static_file(path, root=STATIC_PATH, download=f)

# @route('/test')
# def test():
#     return request.query.size;

bottle.debug(True)
app = bottle.default_app()

#if __name__ == '__main__':
#    bottle.run(host='localhost', port=8000, debug=True, reloader=True)

