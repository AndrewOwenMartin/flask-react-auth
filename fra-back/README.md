# fra-back

A part of [Flask React Authentication](../) example app.

A flask app, reliant on these libraries installed with pip:
 - `Flask-Dance`: Handles OAuth for us, installed with `pip install Flask-Dance[sqla]`
 - `SQLAlchemy`: Handles storage of users, roles, and sessions.
 - `Flask-Security`: Handles a lot of business logic we'd have to implement ourselves otherwise.
 - `email_validator`: Required by Flask-Security, but not listed as a dependency for some reason.

## templates

The templates directory holds the HTML templates, these were largely copied from the equivalent directory in Microsoft's [https://github.com/Azure-Samples/ms-identity-python-webapp](Azure-Samples/ms-identity-python-webapp)
)
