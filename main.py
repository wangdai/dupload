import bottle
from controller import *

if __name__ == '__main__':
    bottle.run(host='localhost', port=8000, debug=True)

app = bottle.default_app()

