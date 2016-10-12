from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from db import Model, session_factory

class Session(Model):
    __tablename__ = 'bookmark_sessions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    session_key = Column(String, length=255)
    ip_address = Column(String, length=100)

    @staticmethod
    def is_valid(key):
        with session_factory() as sess:
            try:
                sess.query(Session).filter(session_key=key).one()
                return True
            except NoResultFound:
                return False