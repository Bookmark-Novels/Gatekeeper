from sqlalchemy import Column, Integer, String

from modules.db import BaseModel, Model, session_factory

class AccountType(BaseModel, Model):
    __tablename__ = 'bookmark_account_types'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(50))

class Types(object):
    Admin = 1
    Native = 2
    Novel_Updates = 3
    Global_Moderator = 4
    Engineer = 5
