import traceback

from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from modules.db import BaseModel, Model, session_factory
from modules.secrets import secrets
from modules.secure import encrypt, decrypt

class Account(BaseModel, Model):
    __tablename__ = 'bookmark_accounts'

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    password = Column(String(255))
    verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_ip = Column(String(100))

    is_auth = None

    def is_authenticated(self):
        if self.is_auth is not None:
            return self.is_auth

        with session_factory() as sess:
            try:
                sess.query(Account).filter(
                    Account.email==self.email,
                    Account.password==self.password
                ).one()

                self.is_auth = True
                return True
            except NoResultFound:
                self.is_auth = False
                return False
            except:
                traceback.print_exc()
                self.is_auth = False
                return False

    def is_active(self):
        return self.verified and self.is_active

    def is_anonymous(self):
        return self.is_authenticated()

    def get_id(self):
        return unicode(self.id)

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
            email = encrypt(email, secrets.fernet_key)
            
            try:
                account = session.query(Account).filter(
                    Account.email==email
                ).one()

                session.expunge(account)

                return account
            except NoResultFound:
                return None