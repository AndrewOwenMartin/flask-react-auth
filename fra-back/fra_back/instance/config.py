# Server
SERVER = "http://localhost:5001"

# Database
SQLALCHEMY_MASTER_DATABASE_URI = "sqlite:///fra_back/db/db.sqlite3"
SQLALCHEMY_CORPUS_DATABASE_URI_JSON = "[[\"foo\", \"sqlite:///fra_back/db/foo.sqlite3\"], [\"bar\", \"sqlite:///fra_back/db/bar.sqlite3\"], [\"baz\", \"sqlite:///fra_back/db/baz.sqlite3\"]]"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # See
# https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196

# Microsoft
AZURE_OAUTH_CLIENT_ID = "38d63387-7cb0-4620-a539-e9849b5b8b33"

# GitHub
GITHUB_OAUTH_CLIENT_ID = "99ed63e09521e4a8d466"

# Google
GOOGLE_CLIENT_ID = "194323813728-2fraqi1ko6hrmtdhkhrc9j29t2udc8nf.apps.googleusercontent.com"

# Flask-Security
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_CONFIRMABLE = False  # I think this is for email confirmation.

# This enables the fields last_login_at, current_login_at, last_login_ip, current_login_ip, login_count.
SECURITY_TRACKABLE = True
