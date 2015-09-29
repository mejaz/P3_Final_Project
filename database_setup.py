import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Usernames(Base):
	__tablename__ = 'usernames'

	# Creating a class for Table Usernames
	user_id = Column(String, primary_key=True)

class Catagory(Base):
	__tablename__ = 'catagory'
	
	# Creating a class for Table Catagory.
	catagory_id = Column(Integer, primary_key=True)
	catagory_name = Column(String, nullable=False)

class Items(Base):
	__tablename__ = 'items'

	# Creating a class for Table Items
	item_id = Column(Integer, primary_key=True)
	item_name = Column(String, nullable=False, unique=True)
	item_desc = Column(String, nullable=False)
	ipicture = Column(String, nullable=True)
	catagory_id_fk = Column(Integer, ForeignKey('catagory.catagory_id', ondelete="CASCADE"))
	catagory = relationship(Catagory)
	user_id_fk = Column(Integer, ForeignKey('usernames.user_id'))
	usernames = relationship(Usernames)

	@property 
	def serialize(self):

		return {
			'name' : self.item_name,
			'id' : self.item_id,
			'description' : self.item_desc
		}

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)