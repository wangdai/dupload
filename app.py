from bottle import *
from bottle import jinja2_template as template
from config import *
import os
import hashlib

#@route('/<name>')
#def index(name):
#    return template('index.tpl', name=name);

@get('/')
def upload():
    return template('upload.tpl');

@post('/')
def do_upload():
    session = Session()
    try:
        upload = request.files.get('upload')

        # guess the file type
        name, ext = os.path.splitext(upload.filename)
        for cat in CATEGORY:
            if ext in CATEGORY.get(cat):
                break
        if cat is None:
            return template(BAD_REQUEST, "File extension '%s' not allowed" % ext)

        # get the hash value for the first HASH_SIZE bytes
        # and judge if same file exists
        file_bytes = upload.file.read(HASH_SIZE)
        md5_value = hashlib.md5(file_bytes).hexdigest()
        same_item = session.query(Item).filter_by(hash_value=md5_value).first()
        if same_item is not None:
            return template("Your file '%s' already exists" % upload.filename, same_item.hash_name)

        item = Item()
        item.category = cat
        item.hash_value = md5_value
        item.hash_name = md5_value[8:24] + ext
        item.origin_name = upload.filename

        session.add(item)
        session.commit()

        save_path = '%s/%s' % (STATIC_PATH, cat)
        upload.save(save_path)
        return 'OK'
    except:
        session.rollback()
        raise
    finally:
        session.close()

#run(server='gunicorn', host='localhost', port=8000)
if __name__ == '__main__':
    run(host='localhost', port=8000)

app = default_app()
