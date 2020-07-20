
import flask
import flask_sqlalchemy

# please the instantiation of app here, it's required to make flask_sqlalchemy work
app = flask.Flask(__name__)

app.config.from_pyfile("instance/config.py", silent=True)

# please the instantiation of app here, it's required to make flask_sqlalchemy work
db = flask_sqlalchemy.SQLAlchemy(app)
