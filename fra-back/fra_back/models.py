import logging
import flask_security
from fra_back.app_init import db

log = logging.getLogger(__name__)


class RoleUsers(db.Model):

    __tablename__ = "roles_users"

    user_id = db.Column(db.ForeignKey("user.id"), primary_key=True, index=True)

    role_id = db.Column(db.ForeignKey("role.id"), primary_key=True, index=True)

    __table_args__ = (db.Index("ix_roles_users_user_2_role_id", "user_id", "role_id"),)


class Role(db.Model, flask_security.RoleMixin):

    __tablename__ = "role"

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(80), unique=True)

    description = db.Column(db.String(255))


class User(db.Model, flask_security.UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True)

    password = db.Column(db.String(255))

    active = db.Column(db.Boolean())

    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship(Role, secondary="roles_users", backref="users")

    last_login_at = db.Column(db.DateTime())

    current_login_at = db.Column(db.DateTime())

    last_login_ip = db.Column(db.String(100))

    current_login_ip = db.Column(db.String(100))

    login_count = db.Column(db.Integer)

    # Can use this to override the 'security payload'
    # def get_security_payload(self):

    #    return {
    #        'id': self.id,
    #        'name': self.name,
    #        'email': self.email
    #    }


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-4s %(name)s %(message)s",
        style="%",
    )

    main()
