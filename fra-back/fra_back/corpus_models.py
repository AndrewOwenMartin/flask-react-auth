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

    engine = session.get_bind()

    app_log.info("creating corpus database: %s", engine)

    Base.metadata.create_all(engine)

class Name(Base):
    
    __tablename__ = "name"

    id = sql.Column(sql.Integer(), primary_key=True)

    name = sql.Column(sql.String(80), unique=True)
