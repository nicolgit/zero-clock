from threading import Thread
from flask import Flask, render_template

class ZeroServer:

    def __init__(self, port):
        self.port = port
        
    def Start(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            return "<html><head><meta http-equiv='refresh' content='0;URL=\"/static/index.html\"' /></head></html>"

        kwargs = {'host': '0.0.0.0', 'port': self.port, 'threaded': True, 'use_reloader': False, 'debug': False}
        laskThread = Thread(target=app.run, daemon=True, kwargs=kwargs).start()

    