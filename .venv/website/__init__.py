from flask import Flask
from .views import views
def app():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix='/')
    app.secret_key = 'wserjkfgyhsduigh'
    return app