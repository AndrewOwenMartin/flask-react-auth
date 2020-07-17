# fra-back

A part of [Flask React Authentication](../) example app.

A flask app, reliant on these libraries installed with pip:
 - [`Flask-Security`](https://pythonhosted.org/Flask-Security/index.html): Handles a lot of business logic we'd have to implement ourselves otherwise.
 - [`Flask-SQLAlchemy-Session`](https://flask-sqlalchemy-session.readthedocs.io/en/v1.1/#comparison-with-flask-sqlalchemy): To handle SQLAlchemt sessions in flask.
 - `SQLAlchemy`: Handles storage of users, roles, and sessions.
 - `email_validator`: Required by Flask-Security, but not listed as a dependency for some reason.

I think I'll also use this, but not sure yet.
 - [`Flask-Dance`](https://flask-dance.readthedocs.io/en/latest/): Handles OAuth for us, installed with `pip install Flask-Dance[sqla]`

## First, let's have an example using Flask-Dance to authenticate.

In `fra_back.app` we make a reference to an oauth provider, in this case google, and a route which has a check for `google.authorised` and on fail, redirects to `url_for("google.login")` and on success responds with a JSONification of the data at `google.get("/oauth2/v1/userinfo")`. As the Flask blueprint returned by `fra_back.app_helpers.make_google_blueprint` has the scope `["profile", "email"]` then we get a response with the keys: `["id", "email", "verified_email", "name", "given_name", "family_name", "locale", "picture"]` for my personal GMail, and the same plus `"hd"` for my GSuite account.

This allows me to pass this data into templates and to check that the user has logged in with a valid Google account. Note, this does not have anything to do with authentication of local users under `current_user.is_authenticated`, just that the app currently has access to at least one google account. The next step is to make the local user authentication receive info from the Google account.

## templates

The templates directory holds the HTML templates, these were largely copied from the equivalent directory in Microsoft's [Azure-Samples/ms-identity-python-webapp](https://github.com/Azure-Samples/ms-identity-python-webapp).
