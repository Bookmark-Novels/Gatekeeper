from datetime import datetime
import traceback
import uuid

from sqlalchemy import  Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from models.accounttype import Types
from modules.db import BaseModel, Model, session_factory
from modules.secrets import secrets

class Account(BaseModel, Model):
    __tablename__ = 'bookmark_accounts'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    account_type = Column(Integer, default=Types.Native)
    timezone = Column(String(100))
    created_at = Column(DateTime)
    last_updated = Column(DateTime)

    is_auth = None

    def is_active(self):
        return self.verified and self.is_active

    @staticmethod
    def from_id(id):
        with session_factory() as sess:
            try:
                account = sess.query(Account).filter(
                    Account.id==id
                ).one()

                sess.expunge(account)

                return account
            except NoResultFound:
                return None

    @staticmethod
    def from_email(email):
        with session_factory() as sess:
            try:
                account = sess.query(Account).filter(
                    Account.email==email
                ).one()

                sess.expunge(account)

                return account
            except NoResultFound:
                return None

    @staticmethod
    def create(name, email, password):
        now = datetime.utcnow()
        acc = Account(
            display_name=name,
            email=email,
            password=password,
            timezone='N/A',
            created_at=now,
            last_updated=now,
            account_type=Types.Native
        ).save()

        return Account.from_email(email).id
