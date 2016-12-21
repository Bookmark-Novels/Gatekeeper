from datetime import datetime, timedelta
import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from modules.db import BaseModel, Model, session_factory

class Nonce(BaseModel, Model):
    __tablename__ = 'bookmark_nonces'

    id = Column(Integer, primary_key=True)
    nonce = Column(String(100))
    origin = Column(String(100))
    is_active = Column(Boolean)
    expires = Column(DateTime)

    @staticmethod
    def use(test, origin):
        with session_factory() as sess:
            try:
                n = sess.query(Nonce).filter(
                    Nonce.nonce==test,
                    Nonce.origin==origin,
                    Nonce.is_active==True,
                    Nonce.expires > datetime.utcnow()
                ).one()

                n.is_active = False
                n.save()

                return True
            except NoResultFound:
                return False

    @staticmethod
    def create(origin):
        nonce = uuid.uuid4()

        Nonce(
            nonce=nonce,
            origin=origin,
            is_active=True,
            expires=datetime.utcnow() + timedelta(minutes=5)
        ).save()

        return nonce
