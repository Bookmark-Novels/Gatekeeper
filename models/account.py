import traceback

from sqlalchemy import  Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from models.accounttype import Types
from modules.db import BaseModel, Model, session_factory
from modules.secrets import secrets

class Account(BaseModel, Model):
    __tablename__ = 'bookmark_accounts'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255))
    snowflake = Column(Integer)
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
        with session_factory() as session:
            try:
                account = session.query(Account).filter(
                    Account.id==id
                ).one()

                session.expunge(account)

                return account
            except NoResultFound:
                return None

    @staticmethod
    def from_email(email):
        with session_factory() as session:
            try:
                account = session.query(Account).filter(
                    Account.email==email
                ).one()

                session.expunge(account)

                return account
            except NoResultFound:
                return None
