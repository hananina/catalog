#config
import os

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


##class
class Category(Base):

    #table
    __tablename__ = 'category'


    # mapper
    name = Column (
      String(80), nullable = False)

    id = Column ( 
      Integer, primary_key = True)


class Item(Base):

    #table
    __tablename__ = 'item'

    # mapper
    name = Column (
      String(80), nullable = False)

    id = Column (
      Integer, primary_key = True)

    created_date = Column(DateTime, default=datetime.utcnow())

    description = Column (
      String(1000))

    category_id = Column(
      Integer, ForeignKey('category.id'))

    category = relationship(Category)


####insert at end of file#####
engine = create_engine(
  'sqlite:///catalog.db'
  )

#which goes into the db and adds the classes 
#we will soon create as new tables in our database.
Base.metadata.create_all(engine)
