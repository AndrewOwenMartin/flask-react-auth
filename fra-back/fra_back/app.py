import flask_dance.contrib.google as google_dance
import flask_dance.contrib.azure as azure_dance
import flask_security
import logging
import flask
import flask_sqlalchemy
import flask_dance.consumer
import fra_back.app_init
import oauthlib.oauth2.rfc6749.errors
import fra_back.models

app, db, log, mail, blueprints = fra_back.app_init.exports

# user_datastore = flask_security.SQLAlchemyUserDatastore(
#    db, fra_back.models.User, fra_back.models.Role
# )
user_datastore = flask_security.SQLAlchemySessionUserDatastore(
    db.session, fra_back.models.User, fra_back.models.Role
)

security = flask_security.Security(app, user_datastore)


@app.before_first_request
def init_data():
    log.info("Attempting to create db at %s", app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()
    if not db.session.query(fra_back.models.User).count():
        user = dict(email="matt@nobien.net", password="password")
        user_datastore.create_user(**user)
        log.info("created user: %s", user)
        db.session.commit()


@app.context_processor
def inject_globals():
    """ Add 'providers' to the context of each template """

    providers = [
        ("Google", flask.url_for("google.login")),
        ("Azure", flask.url_for("azure.login")),
    ]

    provider2info = {
        "google": ("Google", "/oauth2/v1/userinfo"),
        "azure": ("Microsoft/Azure", "/v1.0/me"),
    }

    def get_auth_info(name, provider):

        authorized = provider.authorized

        nice_name, url = provider2info[name]

        auth_data = {"authorized": authorized, "name": nice_name}

        info = {}

        if authorized:

            try:

                response = provider.get(url)

            except oauthlib.oauth2.rfc6749.errors.TokenExpiredError as err:

                info["error"] = str(err)

            else:

                if response.ok:

                    info = response.json()

                else:

                    info["error"] = "response.ok was falsy"

        auth_data["info"] = info

        return auth_data

    auth_data = [
        get_auth_info(name, provider)
        for name, provider in (
            ("google", google_dance.google),
            ("azure", azure_dance.azure),
        )
    ]

    return dict(providers=providers, auth_data=auth_data)


@app.route("/")
def index():

    flask.flash("This is a flask.flash test")

    log.info("This is a log.info test")

    return flask.render_template("index.html")


@app.route("/show-config/")
def show_config():
    return flask.render_template("show-config.html")


@app.route("/user/")
@flask_security.login_required
def user():
    return "only logged in users should see this"


@app.route("/select-oauth-provider/")
def select_oauth_provider():

    return flask.render_template("login.html")


@app.route("/oauth-status/")
def oauth_status():

    google_auth_data = {"logged_in": "no"}
    azure_auth_data = {"logged_in": "no"}

    if google_dance.google.authorized:

        try:

            google_response = google_dance.google.get("/oauth2/v1/userinfo")

        except oauthlib.oauth2.rfc6749.errors.TokenExpiredError:

            google_auth_data["msg"] = "get raised TokenExpiredError"

        else:

            if google_response.ok:

                google_auth_data = google_response.json()

            else:

                google_auth_data["msg"] = "response.ok was falsy"

    if azure_dance.azure.authorized:

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


@flask_dance.consumer.oauth_authorized.connect_via(blueprints["google"])
def google_logged_in(blueprint, token):

    log.info("google_logged_in runs")

    if not token:

        flask.flash("failed to log in with google", category="error")
        log.info("not token")

        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")

    if not resp.ok:

        msg = "Failed to fetch user info from Google."

        flask.flash(msg, category="error")
        log.info("not resp.ok")

        return False

    log.info("resp.ok! %s", str(resp.json()))
    flask.flash(str(resp.json()))

    return False
