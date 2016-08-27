from flask import Flask
from flask import render_template


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "a389ajgo9284tu"


from src.common.database import Database
@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')

from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.users.views import user_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(alert_blueprint, url_prefix='/alert')