import flask_dance.contrib.google as google_dance
import flask_dance.contrib.azure as azure_dance
import flask_dance.contrib.github as github_dance
import flask_security
import logging
import flask
import flask_dance.consumer
import fra_back.app_init
import oauthlib.oauth2.rfc6749.errors
import fra_back.models
import flask_sqlalchemy_session
import sqlalchemy as sql
import sqlalchemy.orm as orm
import json
import functools
import random
import string

app, master_session, log, mail, user_datastore = fra_back.app_init.exports

@app.before_first_request
def init_data():
    fra_back.models.create_all(master_session)

    init_corpora = json.loads(app.config["SQLALCHEMY_CORPUS_DATABASE_URI_JSON"])

    for name, path in init_corpora:
        corpus_q = (
            master_session
            .query(fra_back.models.Corpus)
            .filter_by(name=name)
        )
        if not corpus_q.count():
            log.info("adding row to corpus table name=%s, path=%s", name, path)
            master_session.add(
                fra_back.models.Corpus(
                    name=name,
                    path=path,
                )
            )

    init_roles = [
        ("assign roles", "can grant roles to other users"),
        ("delete user", "can delete users"),
        ("read_foo", "can read from the corpus foo"),
        ("read_bar", "can read from the corpus bar"),
        ("read_baz", "can read from the corpus baz"),
    ]

    for name, description in init_roles:

        role_q = (
            master_session
            .query(fra_back.models.Role)
            .filter_by(name=name)
        )

        if not role_q.count():
            log.info("adding row to row table name=%s, description=%s", name, description)
            master_session.add(
                fra_back.models.Role(
                    name=name,
                    description=description,
                )
            )
            
    master_session.commit()

    corpora_q = (
        master_session.query(fra_back.models.Corpus)
    )

    corpus_sessions = {}

    for corpus in corpora_q:
        engine = sql.create_engine(corpus.path)
        corpus_session_factory = orm.sessionmaker(bind=engine)
        corpus_session = flask_sqlalchemy_session.flask_scoped_session(corpus_session_factory, app)
        log.info("storing scoped session (%s) for corpus %s", corpus_session, corpus.name)
        corpus_sessions[corpus.name] = corpus_session

    app.corpus_sessions = corpus_sessions
    #if not session.query(fra_back.models.User).count():
    #    user = dict(email="matt@nobien.net", password="password")
    #    user_datastore.create_user(**user)
    #    log.info("created user: %s", user)
    #    session.commit()


@app.context_processor
def inject_globals():
    """ Add 'providers' to the context of each template """

    providers = [
        ("Google", flask.url_for("google.login")),
        ("Azure", flask.url_for("azure.login")),
        ("GitHub", flask.url_for("github.login")),
    ]

    provider2info = {
        "google": ("Google", "/oauth2/v1/userinfo"),
        "azure": ("Microsoft/Azure", "/v1.0/me"),
        "github": ("GitHub", "/user"),
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
            ("github", github_dance.github),
        )
    ]

    return dict(providers=providers, auth_data=auth_data)


@app.route("/")
def index():

    # https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
    #flask.flash("This is a flask.flash test")

    #log.info("This is a log.info test")


    user_list = master_session.query(fra_back.models.User).options(orm.joinedload('oauth')).all()

    role_list = master_session.query(fra_back.models.Role).all()

    #current_session = flask_sqlalchemy_session.current_session

    # user_list = current_session.query(fra_back.models.User).all()

    #role_list = current_session.query(fra_back.models.Role).all()

    return flask.render_template("index.html", user_list=user_list, role_list=role_list)


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

    return flask.render_template("login-required.html")

def get_auth_data(get_response):

    response = get_response()

    if not response.ok:

        response_data = None

    else:

        response_data = response.json()

    return response_data

def handle_oauth_authorization(blueprint, token, url, id_key="id", name_key="name"):

    provider_name = blueprint.name

    log.info("handle oauth for %s", provider_name)

    if not token:

        msg = f"failed to log in with {provider_name}"

        log.info("not token: %s", msg)

        return False

    auth_data = get_auth_data(
        get_response=functools.partial(blueprint.session.get, url=url),
    )

    if auth_data is None:

        msg = f"Failed to fetch user info from {provider_name}"

        log.info("not resp.ok: %s", msg)

        return False

    try:

        provider_user_id = str(auth_data[id_key])

    except KeyError:

        raise KeyError(f"Expected '{id_key}', for the provider_user_id field, but only found {sorted(auth_data)}.")

    try:

        provider_user_name = str(auth_data[name_key])

    except KeyError:

        raise KeyError(f"Expected '{name_key}', for the provider_user_name field, but only found {sorted(auth_data)}.")

    if not provider_user_name:

        provider_user_name = "default name"

        log.info("Which is the name field?: %s", auth_data)

    # Do we already have Oauth for this user/provider combination?
    oauth_q = (
        master_session
        .query(
            fra_back.models.OAuth
        )
        .filter(
            fra_back.models.OAuth.provider==provider_name,
            fra_back.models.OAuth.key==provider_user_id,
        )
    )

    try:

        # Yes, let's keep a reference to it,
        oauth = oauth_q.one()
        log.info("found an instance of oauth for provider=%s, key=%s", provider_name, provider_user_id)

    except orm.exc.NoResultFound:

        # No, let's make a record of it.
        oauth = fra_back.models.OAuth(
            provider=provider_name,
            key=provider_user_id,
            token=token,
        )
        log.info("made a new instance of oauth for provider=%s, key=%s", provider_name, provider_user_id)

    user = oauth.user

    # Have we already registered a local user to this user/provider pair
    if user:

        # Yes, log it in.
        flask_security.login_user(user)
        #user_datastore.activate_user(user)
        log.info("Successfully logged in as user: %s (%s)", user.to_log(), provider_name)

    else:

        # No, make the user, then log it in.

        # This manually makes the user, but I don't think I want that.
        # user = fra_back.models.User(
        #     name=provider_user_name,
        #     email="".join(random.choice(string.printable[:62]) for num in range(100)),
        # )

        # Make a user using user_datastore, but that uses flask-sqlalchemy, and
        # I don't think I want that.
        user = user_datastore.create_user(
            name=provider_user_name,
            email="".join(random.choice(string.printable[:62]) for num in range(100)),
        )

        user_datastore.activate_user(user)

        oauth.user=user

        # Note that if we just created this OAuth token, then it can't
        # have an associated local account yet. So we don't need to handle the
        # session.add and session.commit for the case where just the oauth is
        # created, because if the oauth is new, the user is also new.
        master_session.add_all([user, oauth])
        master_session.commit()
        log.info("Made a new user '%s' (%s), then signed in as %s (%s)", provider_user_name, provider_user_id, user.to_log(), provider_name)
        flask_security.login_user(user)

    #security.datastore.commit()
    master_session.commit()

    # Since we're manually creating the OAuth model in the database,
    # we should return False so that Flask-Dance knows that
    # it doesn't have to do it. If we don't return False, the OAuth token
    # could be saved twice, or Flask-Dance could throw an error when
    # trying to incorrectly save it for us.
    return False

# @flask_dance.consumer.oauth_authorized.connect_via(app.blueprints["azure"])
# def azure_logged_in(blueprint, token):
# 
#     return handle_oauth_authorization(blueprint, token, url="/v1.0/me", id_key="id", name_key="userPrincipalName")
# 
# @flask_dance.consumer.oauth_authorized.connect_via(app.blueprints["github"])
# def github_logged_in(blueprint, token):
# 
#     return handle_oauth_authorization(blueprint, token, url="/user", id_key="id", name_key="name")
# 
# @flask_dance.consumer.oauth_authorized.connect_via(app.blueprints["google"])
# def google_logged_in(blueprint, token):
# 
#     return handle_oauth_authorization(blueprint, token, url="/oauth2/v1/userinfo", id_key="id", name_key="name")
