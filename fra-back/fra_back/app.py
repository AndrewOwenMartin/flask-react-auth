import flask_dance.contrib.google as google_dance
import flask_dance.contrib.azure as azure_dance
import flask_security
import logging
import flask
import flask_sqlalchemy
import fra_back.app_init
import oauthlib.oauth2.rfc6749.errors
import fra_back.models

app, db, log = fra_back.app_init.exports

user_datastore = flask_security.SQLAlchemyUserDatastore(
    db, fra_back.models.User, fra_back.models.Role
)

security = flask_security.Security(app, user_datastore)


@app.before_first_request
def init_data():
    log.info("Attempting to create db at %s", app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()
    user_datastore.create_user(email="matt@nobien.net", password="password")
    db.session.commit()


@app.context_processor
def inject_globals():
    """ Add 'providers' to the context of each template """

    providers = [
        ("Google", flask.url_for("google.login")),
        ("Azure", flask.url_for("azure.login")),
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

    google_auth_data = {"logged_in": "no"}
    azure_auth_data = {"logged_in": "no"}

    try:

        google_response = google_dance.google.get("/oauth2/v1/userinfo")

    except oauthlib.oauth2.rfc6749.errors.TokenExpiredError:

        google_auth_data["msg"] = "get raised TokenExpiredError"

    else:

        if google_response.ok:

            google_auth_data = google_response.json()

        else:

            google_auth_data["msg"] = "response.ok was falsy"

    try:

        azure_response = azure_dance.azure.get("/v1.0/me")

    except oauthlib.oauth2.rfc6749.errors.TokenExpiredError:

        azure_auth_data["msg"] = "get raised TokenExpiredError"

    else:

        if azure_response.ok:

            azure_auth_data = azure_response.json()

        else:

            azure_auth_data["msg"] = "response.ok was falsy"
    return flask.render_template(
        "login-required.html",
        google_auth_data=google_auth_data,
        azure_auth_data=azure_auth_data,
    )
