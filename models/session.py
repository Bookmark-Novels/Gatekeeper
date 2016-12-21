from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from modules.db import BaseModel, Model, session_factory

class Session(BaseModel, Model):
    __tablename__ = 'bookmark_sessions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    session_key = Column(String(255))
    ip_address = Column(String(100))
    last_use = Column(DateTime)
    is_active = Column(Boolean)

    @staticmethod
    def is_valid(key):
        with session_factory() as sess:
            try:
                sess.query(Session).filter(
                    Session.session_key==key,
                    Session.is_active==True
                ).one()
                return True
            except NoResultFound:
                return False

    @staticmethod
    def from_key(key):
        with session_factory() as sess:
            try:
                session = sess.query(Session).filter(
                    Session.session_key==key,
                ).one()
                sess.expunge(Session)
                return session
            except NoResultFound:
                return None

    def update_ip(ip):
        self.ip_address = ip
        self.save()

    def use(self):
        if self.is_active:
            self.last_use = datetime.utcnow()
            self.save()
            return True
        return False

    @staticmethod
    def create(account_id, ip):
        session_key = uuid.uuid4()

        Session(
            account_id=account_id,
            session_key=session_key,
            ip_address=ip,
            last_use=datetime.utcnow(),
            is_active=True
        ).save()

        return session_key
