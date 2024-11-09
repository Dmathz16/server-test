import os
from flask import Flask

from application.views.page1 import page1
from application.views.page2 import page2


def create_app():
    app = Flask(__name__) 
    
    app.register_blueprint(page1)
    app.register_blueprint(page2)

    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')