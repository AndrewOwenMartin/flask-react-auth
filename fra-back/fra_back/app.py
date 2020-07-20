# import collections, datetime, functools, itertools
# import json, logging, pathlib, random, re
# import flask
# import flask_sqlalchemy
# #import fra_back.models as models
# import fra_back.app_helpers as app_helpers
# import flask_dance.contrib.google as google_dance
# import flask_dance.contrib.azure as azure_dance
# import flask_security
# import subprocess
# #import fra_back.models as db
# from logging import DEBUG, INFO, WARNING, ERROR, FATAL
# 
# SILENT = 0
#from fra_back.app_init import app, db
#from fra_back import models
#from fra_back.models import Role, User
import logging
import flask
import flask_sqlalchemy
from fra_back.app_init import app, db
import fra_back.models

app.logger.setLevel(logging.DEBUG)

# user_datastore = flask_security.SQLAlchemyUserDatastore(db, User, Role)
# 
# security = flask_security.Security(app, user_datastore)
# 
#app.register_blueprint(
#    app_helpers.make_google_blueprint(config=app.config), url_prefix="/login"
#)
#app.register_blueprint(
#    app_helpers.make_azure_blueprint(config=app.config), url_prefix="/login"
#)

    #return app, db, app.logger, user_datastore

    # app.engine = sql.create_engine("sqlite:///fra_back/db.sqlite3")

    # user_datastore, security = app_helpers.make_security(
    #     session=app.session, user_model=db.User, role_model=db.Role
    # )

    # security.init_app(app, user_datastore)

    # app.secret_key = app.config.get("SECRET_KEY")


log = app.logger

@app.before_first_request
def init_data():
    log.info("Attempting to create db at %s", app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()


@app.context_processor
def inject_globals():
    """ Add 'providers' to the context of each template """

    providers = [
        #("Google", flask.url_for("google.login")),
        #("Azure", flask.url_for("azure.login")),
    ]

    return dict(providers=providers)


@app.route("/")
def index():

    return flask.render_template("index.html")


@app.route("/show-config/")
def show_config():
    return flask.render_template("show-config.html")


@app.route("/user/")
def user():
    return "only logged in users should see this"


@app.route("/login/")
def login():

    return flask.render_template("login.html")


@app.route("/login-required/")
def login_required():

    #if not app_helpers.is_authorized_any():

    #    login_url = flask.url_for("login")

    #    log.info("redirecting to 'choose your provider' login url: %s", login_url)

    #    return flask.redirect(login_url)

    #google_response = google_dance.google.get("/oauth2/v1/userinfo")

    #log.info(
    #    "Authorized: %s. Response is OK: %s",
    #    google_dance.google.authorized,
    #    google_response.ok,
    #)

    #if google_response.ok:

    #    google_auth_data = google_response.json()

    #else:

    #    google_auth_data = {"logged_in": "no", "msg": "response.ok was falsy"}

    #google_picture = google_auth_data.setdefault("picture", None)

    ## azure_response = azure_dance.azure.get("https://graph.microsoft.com/v1.0/users")
    #azure_response = azure_dance.azure.get("/v1.0/me")

    #if azure_response.ok:

    #    azure_auth_data = azure_response.json()

    #else:

    #    azure_auth_data = {"logged_in": "no", "msg": "response.ok was falsy"}

    return flask.render_template(
        "login-required.html",
        google_auth_data={},
        google_picture=None,
        azure_auth_data={},
    )


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
