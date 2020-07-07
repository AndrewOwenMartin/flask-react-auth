import collections, datetime, functools, itertools
import json, logging, pathlib, random, re

import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative

import flask_security
import flask_dance.consumer.storage.sqla

from logging import DEBUG, INFO, WARNING, ERROR, FATAL
SILENT = 0

log = logging.getLogger(__name__)

Base = sqlalchemy.ext.declarative.declarative_base()

class RoleUsers(Base):

    __tablename__ = "roles_users"

    user_id = sql.Column(sql.ForeignKey("user.id"), primary_key=True, index=True)

    role_id = sql.Column(sql.ForeignKey("role.id"), primary_key=True, index=True)

    __table_args__ = (
        sql.Index(
            "ix_roles_users_user_2_role_id", "user_id", "role_id"
        ),
    )

class Role(Base, flask_security.RoleMixin):
    
    __tablename__ = "role"

    id = sql.Column(sql.Integer(), primary_key=True)
    name = sql.Column(sql.String(80), unique=True)
    description = sql.Column(sql.String(255))

class User(Base, flask_security.UserMixin):

    __tablename__ = "user"

    id = sql.Column(sql.Integer, primary_key=True)

    email = sql.Column(sql.String(255), unique=True)

    password = sql.Column(sql.String(255))

    active = sql.Column(sql.Boolean())

    confirmed_at = sql.Column(sql.DateTime())

    roles = orm.relationship(
        Role, secondary="roles_users", backref="users"
    )


class OAuth(Base, flask_dance.consumer.storage.sqla.OAuthConsumerMixin):
    provider_user_id = sql.Column(sql.String(256), unique=True, nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey(User.id), nullable=False)
    user = orm.relationship(User)


def create_new_db(path="sqlite:///fra_back/db.sqlite3"):

    engine = sql.create_engine(path)

    Base.metadata.create_all(engine)

    log.info("created db at: %s", path)

def main():

    create_new_db()


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    main()
