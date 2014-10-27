import bottle
from bottle import route, run, get, post, request
from bottle import jinja2_template as template
import os

@route('/<name>')
def index(name):
    return template('index.tpl', name=name);

@get('/upload')
def upload():
    return template('upload.tpl');

@post('/upload')
def do_upload():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in('.png', '.jpg', '.gif'):
        return 'File extension not allowed.'
    
    save_path = '/home/wangdai/www/'
    upload.save(save_path)
    return 'OK'

#run(server='gunicorn', host='localhost', port=8000)
if __name__ == '__main__':
    run(host='localhost', port=8000)

app = bottle.default_app()
