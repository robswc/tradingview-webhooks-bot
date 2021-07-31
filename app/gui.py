from flask import Flask
from werkzeug.exceptions import NotFound
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from components.interface import server
from server import app

# logging
import logging

# settings
from components.settings import interface_base

flask_app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

flask_app.wsgi_app = DispatcherMiddleware(NotFound(), {
    "/{}".format(interface_base): server,
    "": app,
})

if __name__ == "__main__":
    print('Starting Server on: {}'.format('http://127.0.0.1:5000/'))
    flask_app.run(debug=True)