from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bae.core import const

engine = create_engine('mysql://%s:%s@%s:%d/AYgoKHBJYtTMvLqJBPmy' % (const.MYSQL_USER, const.MYSQL_PASS, const.MYSQL_HOST, int(const.MYSQL_PORT)),
    convert_unicode=True,
    pool_recycle=25)

db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

"""
初始化数据库，添加ORM映射。
"""
def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import model
    Base.metadata.create_all(bind=engine)
