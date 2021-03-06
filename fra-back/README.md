# fra-back

A part of [Flask React Authentication](../) example app.

A flask app, reliant on these libraries installed with pip:
 - [`Flask-Security`](https://pythonhosted.org/Flask-Security/index.html): Handles a lot of business logic we'd have to implement ourselves otherwise.
 - [`Flask-SQLAlchemy-Session`](https://flask-sqlalchemy-session.readthedocs.io/en/v1.1/#comparison-with-flask-sqlalchemy): To handle SQLAlchemt sessions in flask.
 - `SQLAlchemy`: Handles storage of users, roles, and sessions.
 - `email_validator`: Required by Flask-Security, but not listed as a dependency for some reason.
 - [`Flask-Dance`](https://flask-dance.readthedocs.io/en/latest/): Handles OAuth for us, installed with `pip install Flask-Dance[sqla]`
 - `bcrypt`: Else flask security can't hash passwords.

## Microsoft integration - Coding the Flask App

In `fra_back.app_helpers` I made the Azure blueprint using `make_azure_blueprint` from `flask_dance.contrib.azure`, the required args were:
 - `client_id`:  the client id of the app `fra-back` created above.
 - `client_secret`: the secret created above.
 - `scope`: `["https://graph.microsoft.com/.default"]` the scopes are actually defined on Azure's side.
 - `redirect_to`: `login_required`, the name of the function which renders the page that should appear after authentication.

In `fra_back.app` I registered the blueprint.

I added a url to `flask.url_for('azure.login')` in the list of providers (injected into all templates with `app.inject_globals`, but didn't use the auth data at all.

## Google integration - Resulting flow

In `fra_back.app` we make a reference to an oauth provider, in this case google, and a route which checks any form of authentication has been made. On fail it redirects to `url_for("login")` and on success it responds with a JSONification of the data at `google.get("/oauth2/v1/userinfo")`.

As the Flask blueprint returned by `fra_back.app_helpers.make_google_blueprint` has the scope `["profile", "email"]` then we get a response with the keys: `["id", "email", "verified_email", "name", "given_name", "family_name", "locale", "picture"]` for my personal GMail, and the same plus `"hd"` for my GSuite account.

This allows me to pass this data into templates and to check that the user has logged in with a valid Google account. Note, this does not have anything to do with authentication of local users under `current_user.is_authenticated`, just that the app currently has access to at least one google account. The next step is to make the local user authentication receive info from the Google account.

# SQLAlchemy integration

I made the system use `flask-sqlalchemy`. I had a lot of trouble getting [`db.create_all()`](./fra_back/app.py#L23) working.
The documentation and stackoverflow suggested it was to do with the order of imports and initialisation.
I had to split `app.py` into [`app.py`](./fra_back/app.py) and [`app_init.py`](./fra_back/app.py) to avoid circular imports.

## templates

The templates directory holds the HTML templates, these were largely copied from the equivalent directory in Microsoft's [Azure-Samples/ms-identity-python-webapp](https://github.com/Azure-Samples/ms-identity-python-webapp).
