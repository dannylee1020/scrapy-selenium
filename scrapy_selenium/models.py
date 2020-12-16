from sqlalchemy import create_engine, Column, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer
from sqlalchemy.engine.url import URL
import scrapy_selenium.settings as settings

Base = declarative_base()

def init_db():
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    return Base.metadata.create_all(engine)


class Dribbble(Base):
    __tablename__ = 'designer_info'

    id = Column(Integer, primary_key = True)
    name = Column('designer_name', String(150))
    location = Column('location', String(150))


