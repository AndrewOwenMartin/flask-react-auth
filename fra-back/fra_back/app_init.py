import logging
import flask
import flask_dance.contrib.google as google_dance
import flask_dance.contrib.azure as azure_dance
import flask_dance.contrib.github as github_dance
import flask_security.datastore
import flask_sqlalchemy_session
import sqlalchemy as sql
import sqlalchemy.orm as orm
import fra_back.models
import flask_dance.consumer.storage.sqla


# import flask_mail  # provides flask_mail.Mail, needed when we start sending emails.

# please the instantiation of app here, it's required to make flask_sqlalchemy work.
app = flask.Flask(__name__)
app.config.from_pyfile("instance/config.py", silent=True)
app.config.from_pyfile("instance/secrets.py", silent=True)

engine = sql.create_engine(app.config["SQLALCHEMY_MASTER_DATABASE_URI"])

master_session_factory = orm.sessionmaker(bind=engine)

master_session = flask_sqlalchemy_session.flask_scoped_session(master_session_factory, app)

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
        "redirect_to": "oauth_status",
    }

    blueprint = azure_dance.make_azure_blueprint(**config_kwargs, **kwargs)

    blueprint.storage = flask_dance.consumer.storage.sqla.SQLAlchemyStorage(fra_back.models.OAuth, master_session)

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

    kwargs = {"scope": ["profile", "email"], "redirect_to": "oauth_status"}

    blueprint = google_dance.make_google_blueprint(**config_kwargs, **kwargs)

    blueprint.storage = flask_dance.consumer.storage.sqla.SQLAlchemyStorage(fra_back.models.OAuth, master_session)

    return blueprint

def make_github_blueprint():
    """ Following the instructions at
https://flask-dance.readthedocs.io/en/latest/providers.html#module-flask_dance.contrib.github
"""

    arg_name2config_key = {
        "client_id": "GITHUB_OAUTH_CLIENT_ID",
        "client_secret": "GITHUB_OAUTH_CLIENT_SECRET",
    }

    config_kwargs = populate_config_kwargs(arg_name2config_key, app.config)

    kwargs = {
        #"scope": ["read:user"],
        "scope": ["user:email"],
        "redirect_to": "oauth_status",
    }

    blueprint = github_dance.make_github_blueprint(**config_kwargs, **kwargs)

    blueprint.storage = flask_dance.consumer.storage.sqla.SQLAlchemyStorage(fra_back.models.OAuth, master_session)

    return blueprint


google_blueprint = make_google_blueprint()
azure_blueprint = make_azure_blueprint()
github_blueprint = make_github_blueprint()

app.register_blueprint(google_blueprint, url_prefix="/login")
app.register_blueprint(azure_blueprint, url_prefix="/login")
app.register_blueprint(github_blueprint, url_prefix="/login")

app.logger.setLevel(logging.DEBUG)
#app.logger.info("log name: %s", __name__)

mail = None  # mail = flask_mail.Mail(app)

# The 'User' or 'SessionUser' versions of SQLAlchemyDatastore assume the use of
# flask-sqlalchemy, whereas I should be using just SQLAlchemyUserDatastore.
user_datastore = flask_security.SQLAlchemySessionUserDatastore(
    master_session, fra_back.models.User, fra_back.models.Role
)

user_datastore.user_model.query = master_session.query(fra_back.models.User)
user_datastore.role_model.query = master_session.query(fra_back.models.Role)

#user_datastore = flask_security.SQLAlchemyDatastore(
#    master_session, fra_back.models.User, fra_back.models.Role
#)

#user_datastore = None
security = flask_security.Security(app, datastore=user_datastore)

exports = (app, master_session, app.logger, mail, user_datastore)
