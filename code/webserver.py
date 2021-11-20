from threading import Thread
from flask import Flask, render_template

class ZeroServer:

    def Start(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            return "<html><head><meta http-equiv='refresh' content='0;URL=\"/static/index.html\"' /></head></html>"

        #if __name__ == '__main__':
        #    app.run(debug=False, host='0.0.0.0')
        kwargs = {'host': '0.0.0.0', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}
        laskThread = Thread(target=app.run, daemon=True, kwargs=kwargs).start()

    