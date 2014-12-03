import hashlib
import json

from bottle import route, redirect, request
from bottle import jinja2_template as template
from sqlalchemy.orm import sessionmaker

import config
import service
from models import engine

Session = sessionmaker(bind=engine)

@route('/test/<category>', method='GET')
def test(category):
    if category is 'all':
        print('yes')
    else:
        print('no')
        print(category.encode())


@route('/static/<path:path>', method='GET')
def static(path):
    return static_file(path, root=STATIC_PATH)

@route('/', method='GET')
def index():
    redirect('/items')

@route('/items', method='GET')
def get_items():
    session = Session()
    # current page
    p = request.query.p or 1
    offset = (p - 1) * config.PAGE_SIZE
    # category
    cat = request.query.cat
    cat = None if cat not in config.CAT_KEYS else cat
    rows = service.get_items_count(session, cat)
    # total pages
    tp = rows // config.PAGE_SIZE
    if rows % config.PAGE_SIZE != 0:
        tp += 1
    # q = request.query.q
    param = dict()
    param['p'] = p
    param['tab'] = cat
    param['cats'] = sorted(config.CAT_KEYS)
    param['r'] = rows
    param['tp'] = tp
    param['items'] = service.get_items(session, offset, config.PAGE_SIZE, cat)
    session.close()
    return template('index', param)

@route('/items', method='POST')
def create_item():
    session = Session()
    try:
        upload = request.files.get('upload')
        desc = request.forms.get('description')
        desc = None if not desc else desc

        item = service.create_item(session, upload.file, upload.rawfilename, desc)

        savepath = '%s/%s' % (config.FILE_ROOT, item.cat)
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        upload.filename = item.hashname
        upload.save(savepath)

        return item.id
    except:
        session.rollback()
        raise
    finally:
        session.close()


@route('/items/<id>', method='DELETE')
def delete_item(id):
    session = Session()
    try:
        id = int(id)
        item = session.query(Item).filter_by(id=id).first()
        path = '%s/%s/%s' % (FILE_ROOT, item.cat, item.hashname)
        os.remove(path)
        session.delete(item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

