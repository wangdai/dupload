from bottle import *
from bottle import jinja2_template as template
from sqlalchemy import desc
from config import *
from models import *
import os
import hashlib
import json

@get('/test/<category>')
def test(category):
    if category is 'all':
        print('yes')
    else:
        print('no')
        print(category.encode())

@get('/static/<path:path>')
def static(path):
    return static_file(path, root=STATIC_PATH)

@get('/')
def index():
    return template('index', category=CATEGORY.keys());

@post('/')
def upload():
    session = Session()
    try:
        upload = request.files.get('upload')
        if upload is None:
            abort(400, "Sorry, you didn't pick a file")
        description = request.forms.get('description')
        if description is None:
            description = ''

        # guess the file type
        name, ext = os.path.splitext(upload.filename)
        if ext in ('.gz', '.bz2'):
            ext = os.path.splitext(name)[1] + ext
        in_cat = False
        for cat in CATEGORY:
            if ext in CATEGORY.get(cat):
                in_cat = True
                break
        if not in_cat:
            abort(400, "File extension '%s' not allowed. Allowed: %s" % (ext, CATEGORY))

        # get the hash value for the first HASH_SIZE bytes
        # and judge if same file exists
        file_bytes = upload.file.read(HASH_SIZE)
        md5_value = hashlib.md5(file_bytes).hexdigest()
        same_item = session.query(Item).filter_by(hash_value=md5_value).first()
        if same_item is not None:
            return template('index',
                    error="'%s' already exists => '%s'" % (upload.filename, same_item.origin_name),
                    category=CATEGORY.keys())

        item = Item()
        item.category = cat
        item.hash_value = md5_value
        item.hash_name = md5_value[8:24] + ext
        item.origin_name = upload.filename
        item.description = description

        save_path = '%s/%s' % (FILE_ROOT, cat)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        upload.filename = item.hash_name
        upload.file.seek(0)
        upload.save(save_path)
        item.file_size = os.path.getsize('%s/%s' % (save_path, item.hash_name))

        session.add(item)
        session.commit()

        return template('index',
                success="'%s' uploading succeeds" % item.origin_name,
                category=CATEGORY.keys())
    except:
        session.rollback()
        raise
    finally:
        session.close()

@get('/cat/<category>')
@get('/cat/<category>/<p>')
def items_info(category, p=0):
    category = str(category)
    if category not in CATEGORY.keys() and category != 'all':
        abort(400, "Category '%s' doesn't exist" % category)
    p = int(p)
    p_start = p * PAGE_SIZE
    p_stop = (p + 1) * PAGE_SIZE
    session = Session()
    if category == 'all':
        items = session.query(Item).order_by(desc(Item.upload_time))[p_start:p_stop]
    else:
        items = session.query(Item).filter_by(category=category).order_by(desc(Item.upload_time))[p_start:p_stop]
    session.close()
    response.set_header('Content-Type', 'application/json')
    return json.dumps(items, cls=ItemEncoder)

@route('/item/<h>', method="DELETE")
def delete_item(h):
    session = Session()
    try:
        item = session.query(Item).filter_by(hash_value=h).first()
        item_path = '%s/%s/%s' % (FILE_ROOT, item.category, item.hash_name)
        os.remove(item_path)
        session.delete(item)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

#run(server='gunicorn', host='localhost', port=8000)
if __name__ == '__main__':
    run(host='localhost', port=8000, debug=True)

app = default_app()
