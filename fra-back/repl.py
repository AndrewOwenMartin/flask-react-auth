import configparser
import fra_back.instance.config
import sqlalchemy as sql
import sqlalchemy.orm as orm
import fra_back.models as models
engine = sql.create_engine(fra_back.instance.config.SQLALCHEMY_MASTER_DATABASE_URI)

master_session_factory = orm.sessionmaker(bind=engine)

master_session = master_session_factory()
