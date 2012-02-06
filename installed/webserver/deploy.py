from werkzeug.contrib.fixers import ProxyFix

from app_creator import create_app

app = create_app('etc.settings')[0]
app.wsgi_app = ProxyFix(app.wsgi_app)
