# Server
SERVER = "http://localhost:5001"

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db/db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # See
# https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196

# Microsoft
AZURE_OAUTH_CLIENT_ID = "38d63387-7cb0-4620-a539-e9849b5b8b33"
AZURE_OAUTH_CLIENT_SECRET = ".H8t6-4Oi~vvjh-MsNL.gaP6DcYMi1P6oR"

# Google
GOOGLE_CLIENT_ID = (
    "67742121830-bvd5ab9j87180hg22mqgu8pk75rhba6p.apps.googleusercontent.com"
)
GOOGLE_SECRET = "SBxXnxT_oytQvATcaWmHduw1"

SECRET_KEY = "flkjelkjsflksjeofiudroigursj,fna,lcnlidfgdhtkjasf;lnasc klydhfkasjefjksdrgfilaysi8r4jk"

# Flask-Security
SECURITY_PASSWORD_SALT = "aslkjlsdkfjoidunrkjbg9ousjdld"
SECURITY_PASSWORD_HASH = "bcrypt"
