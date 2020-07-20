import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import flask_dance.contrib.google as google_dance
import flask_dance.contrib.azure as azure_dance
import flask_security.datastore

from logging import DEBUG, INFO, WARNING, ERROR, FATAL

SILENT = 0

log = logging.getLogger(__name__)


def is_authorized_any():

    NAME2OAUTH_PROVIDER = {"google": google_dance.google, "azure": azure_dance.azure}

    auths = {
        name: provider.authorized for name, provider in NAME2OAUTH_PROVIDER.items()
    }

    log = logging.getLogger("app")

    log.info("is_authorized_any: %s", json.dumps(sorted(auths.items())))

    return any(auths.values())


class SQLAlchemySessionDatastore(
    flask_security.datastore.Datastore, flask_security.datastore.UserDatastore
):
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
