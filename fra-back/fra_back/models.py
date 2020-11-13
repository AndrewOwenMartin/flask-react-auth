import logging
import flask_security
import flask_dance.consumer.storage.sqla
import sqlalchemy as sql
import sqlalchemy.ext.declarative
import sqlalchemy.orm as orm

log = logging.getLogger(__name__)

Base = sqlalchemy.ext.declarative.declarative_base()

def create_all(session):

    app_log = logging.getLogger("fra_back.app_init")

    app_log.info("create all info log: XXXXXXXX")

    engine = session.get_bind()

    Base.metadata.create_all(engine)

class RoleUsers(Base):

    __tablename__ = "roles_users"

    user_id = sql.Column(sql.ForeignKey("user.id"), primary_key=True, index=True)

    role_id = sql.Column(sql.ForeignKey("role.id"), primary_key=True, index=True)

    __table_args__ = (sql.Index("ix_roles_users_user_2_role_id", "user_id", "role_id"),)


class Role(Base, flask_security.RoleMixin):

    __tablename__ = "role"

    id = sql.Column(sql.Integer(), primary_key=True)

    name = sql.Column(sql.String(80), unique=True)

    description = sql.Column(sql.String(255))


class User(Base, flask_security.UserMixin):

    __tablename__ = "user"

    id = sql.Column(sql.Integer, primary_key=True)

    email = sql.Column(sql.String(255), unique=True)

    name = sql.Column(sql.String(255))

    active = sql.Column(sql.Boolean())

    confirmed_at = sql.Column(sql.DateTime())

    roles = orm.relationship(Role, secondary="roles_users", backref="users")

    last_login_at = sql.Column(sql.DateTime())

    current_login_at = sql.Column(sql.DateTime())

    last_login_ip = sql.Column(sql.String(100))

    current_login_ip = sql.Column(sql.String(100))

    login_count = sql.Column(sql.Integer)

    def to_log(self):

        return dict(
            id=self.id,
            name=self.name,
        )

    # Can use this to override the 'security payload'
    def get_security_payload(self):

        raise NotImplementedError("don't know who calls this when")

        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class OAuth(Base, flask_dance.consumer.storage.sqla.OAuthConsumerMixin):

    # id = Column(Integer, primary_key=True)
    # provider = Column(String(50), nullable=False)
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # token = Column(MutableDict.as_mutable(JSONType), nullable=False)

    user_id = sql.Column(sql.ForeignKey("user.id"))

    user = orm.relationship(User, backref="oauth")

    key = sql.Column(sql.String(255), unique=True, index=True)

class Corpus(Base):

    __tablename__ = "corpus"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String, unique=True, index=True)
    path = sql.Column(sql.Text)

    def __repr__(self):
        return "<Corpus:{corpus_id} {name}>".format(corpus_id=self.id, name=self.name)

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    main()
