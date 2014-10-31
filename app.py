from bottle import *
from bottle import jinja2_template as template
import os
from config import *

#@route('/<name>')
#def index(name):
#    return template('index.tpl', name=name);

@get('/')
def upload():
    return template('upload.tpl');

@post('/')
def do_upload():
    #session = Session()
    #try:
    upload = request.files.get('upload')
    barr = upload.file.read(1024)
    print(barr)
    print('SIZE=%d' % len(barr))
        #name, ext = os.path.splitext(upload.filename)
        #if ext not in('.png', '.jpg', '.gif'):
        #    return 'File extension not allowed.'
        #
        #save_path = '/home/wangdai/www/'
        #upload.save(save_path)
    #except:
    #    session.rollback()
    #    raise
    #finally:
    #    session.close()
    return 'OK'

#run(server='gunicorn', host='localhost', port=8000)
if __name__ == '__main__':
    run(host='localhost', port=8000)

app = default_app()
