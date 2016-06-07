#config
import os

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


##class
class Shop(Base):

    #table
    __tablename__ = 'shop'


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

    description = Column (String(1000))

    category = Column (String(250))

    shop_id = Column(Integer,ForeignKey('shop.id'))
    shop = relationship(Shop)


####insert at end of file#####
engine = create_engine(
  'sqlite:///catalog.db'
  )

#which goes into the db and adds the classes 
#we will soon create as new tables in our database.
Base.metadata.create_all(engine)
