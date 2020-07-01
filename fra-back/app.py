import collections, datetime, functools, itertools
import json, logging, pathlib, random, re
import flask
from logging import DEBUG, INFO, WARNING, ERROR, FATAL
SILENT = 0

log = logging.getLogger(__name__)

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
