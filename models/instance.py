from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from modules.db import BaseModel, Model, session_factory

class Instance(BaseModel, Model):
    __tablename__ = 'bookmark_instances'

    id = Column(Integer, primary_key=True)
    instance_id = Column(String(50))
    instance_name = Column(String(100))

    @staticmethod
    def exists(instance):
        with session_factory() as sess:
            try:
                sess.query(Instance).filter(
                    Instance.instance_id==instance
                ).one()
                return True
            except NoResultFound:
                return False

    @staticmethod
    def from_id(id):
        with session_factory() as sess:
            try:
                instance = sess.query(Instance).filter(
                    Instance.instance_id==id
                ).one()

                sess.expunge(instance)

                return instance
            except NoResultFound:
                return None
