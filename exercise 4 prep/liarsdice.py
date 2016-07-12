import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///liarsdice.db')


def createDB():
    """Use to initiate database file"""
    Base.metadata.create_all(engine)

def connect():
    """Used in multiple methods to make a database connection"""
    Base.metadata.bind = engine
    return sessionmaker(bind = engine)()

def insert(name):
    session = connect()
    session.add(Restaurant(name = name))
    session.commit()
    print session.query(Restaurant).all()
    cheesepizza = MenuItem(name = 'Cheeze Pizza',
                           description = 'It has a lot of cheese',
                           course = 'Entree', price = '$2.99',
                           restaurant = Restaurant(name = name))
    session.add(cheesepizza)
    session.commit()
    print session.query(MenuItem).all()
    
def read():
    session = connect()
    print session.query(MenuItem).first().name
    items = session.query(Restaurant).all()
    for item in items:
        print item.name

def update(id, newName):
    session = connect()
    foundRestaurant = session.query(Restaurant).filter_by(id = id).one()
    print foundRestaurant.name
    foundRestaurant.name = newName
    session.add(foundRestaurant)
    session.commit()
    foundRestaurant = session.query(Restaurant).filter_by(id = id).one()
    print foundRestaurant.name

def delete(id):
    session = connect()
    foundRestaurant = session.query(Restaurant).filter_by(id = id).one()
    print foundRestaurant.name
    session.delete(foundRestaurant)
    session.commit()
