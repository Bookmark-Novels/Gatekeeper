from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from db import Model, session_factory

class Nonce(Model):
    __tablename__ = 'bookmark_nonces'

    id = Column(Integer, primary_key=True)
    nonce = Column(String, length=100)

    @staticmethod
    def use(test):
        with session_factory() as sess:
            try:
                n = sess.query(nonce).filter(nonce=test).one()
                n.delete()
                return True
            except NoResultFound:
                return False