# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from app import app

manager = Manager(app)
manager.add_command("runserver",
        Server(host="10.0.2.9", port=8000, use_debugger=True))

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True,host='10.0.2.9',port=8000)
