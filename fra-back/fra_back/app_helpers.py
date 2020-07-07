import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import flask_dance.contrib.google as google_dance
import flask_security.datastore

from logging import DEBUG, INFO, WARNING, ERROR, FATAL
SILENT = 0

log = logging.getLogger(__name__)

def make_google_blueprint(config):

    arg_name2config_key = {
        "client_id": "GOOGLE_CLIENT_ID",
        "client_secret": "GOOGLE_SECRET",
    }

    kwargs = {
        arg_name: config.get(config_key)
        for arg_name, config_key
        in arg_name2config_key.items()
    }

    blueprint = google_dance.make_google_blueprint(**kwargs)

    return blueprint

class SQLAlchemySessionDatastore(flask_security.datastore.Datastore, flask_security.datastore.UserDatastore):
    def __init__(self, session, user_model, role_model):
        flask_security.datastore.Datastore.__init__(self, db=session)
        flask_security.datastore.UserDatastore.__init__(self, user_model, role_model)


def make_security(session, user_model, role_model):

    user_datastore = SQLAlchemySessionDatastore(session, user_model, role_model)

    security = flask_security.Security(datastore=user_datastore)

    return user_datastore, security

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

