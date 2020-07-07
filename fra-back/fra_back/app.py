import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import flask
import sqlalchemy as sql
import sqlalchemy.orm as orm
import fra_back.app_helpers as app_helpers
import flask_dance.contrib.google as google_dance
import flask_security
import fra_back.models as db
from logging import DEBUG, INFO, WARNING, ERROR, FATAL
SILENT = 0


def create_app():

    app = flask.Flask(__name__)

    app.config.from_pyfile("instance/config.py", silent=True)

    app.engine = sql.create_engine("sqlite:///fra_back/db.sqlite3")

    app.Sessionmaker = orm.sessionmaker(bind=app.engine)

    app.session = app.Sessionmaker()

    user_datastore, security = app_helpers.make_security(session=app.session, user_model=db.User, role_model=db.Role)

    security.init_app(app, user_datastore)

    app.secret_key = app.config.get("SECRET_KEY")

    app.register_blueprint(app_helpers.make_google_blueprint(config=app.config), url_prefix="/login")

    app.logger.setLevel(logging.DEBUG)

    return app

app = create_app()
log = app.logger

@app.route('/')
def index():

    return flask.render_template("index.html")

@app.route('/show-config/')
def show_config():
    return flask.render_template("show-config.html")

@app.route('/user/')
def user():
    return 'only logged in users should see this'

@app.route('/you-are-logged-in/')
def you_are_logged_in():

    if not google_dance.google.authorized:

        return flask.redirect(flask.url_for("google.login"))

    response = google_dance.google.get("/user")

    log.info("Authorised: %s. Response is OK: %s", google_dance.google.authorized, response.ok)

    if response.ok:

        auth_data = response.json()

    else:

        auth_data = {}

    return flask.render_template("you-are-logged-in.html", auth_data=auth_data)

def main():

    pass

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    main()
