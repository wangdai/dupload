import bottle
from controller import *

bottle.debug(True)
bottle.TEMPLATE_PATH.append('../views/')
app = bottle.default_app()

#if __name__ == '__main__':
#    bottle.run(host='localhost', port=8000, debug=True, reloader=True)

