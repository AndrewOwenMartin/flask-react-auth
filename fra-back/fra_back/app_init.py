import logging
import flask
import flask_sqlalchemy
import flask_dance.contrib.google as google_dance
import flask_dance.contrib.azure as azure_dance

# please the instantiation of app here, it's required to make flask_sqlalchemy work.
app = flask.Flask(__name__)

app.config.from_pyfile("instance/config.py", silent=True)


def populate_config_kwargs(arg_name2config_key, config):

    return {
        arg_name: config.get(config_key)
        for arg_name, config_key in arg_name2config_key.items()
    }


def make_azure_blueprint():
    """ Following the instructions at
https://flask-dance.readthedocs.io/en/latest/providers.html#module-flask_dance.contrib.azure
"""

    arg_name2config_key = {
        "client_id": "AZURE_OAUTH_CLIENT_ID",
        "client_secret": "AZURE_OAUTH_CLIENT_SECRET",
    }

    config_kwargs = populate_config_kwargs(arg_name2config_key, app.config)

    kwargs = {
        "scope": ["https://graph.microsoft.com/.default"],
        "redirect_to": "login_required",
    }

    blueprint = azure_dance.make_azure_blueprint(**config_kwargs, **kwargs)

    return blueprint


def make_google_blueprint():
    """ Following the instructions at
https://flask-dance.readthedocs.io/en/latest/providers.html#module-flask_dance.contrib.google
"""

    arg_name2config_key = {
        "client_id": "GOOGLE_CLIENT_ID",
        "client_secret": "GOOGLE_SECRET",
    }

    config_kwargs = populate_config_kwargs(arg_name2config_key, app.config)

    kwargs = {"scope": ["profile", "email"], "redirect_to": "login_required"}

    blueprint = google_dance.make_google_blueprint(**config_kwargs, **kwargs)

    return blueprint


app.register_blueprint(make_google_blueprint(), url_prefix="/login")
app.register_blueprint(make_azure_blueprint(), url_prefix="/login")

# please the instantiation of db here, it's required to make flask_sqlalchemy work.
db = flask_sqlalchemy.SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)

exports = (app, db, app.logger)
