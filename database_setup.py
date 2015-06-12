# python finalproject.py

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    """Defines class User"""
    __tablename__ = 'user'

    #Define colums
    id = Column(Integer, primary_key=True)
    social_id = Column(String(64), nullable=True, unique=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=True)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'social_id': self.social_id,
           'name': self.name,
           'email': self.email,
           'picture': self.picture,
        }


class Category(Base):
    """Defines class Category"""
    __tablename__ = 'category'

    #Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'id': self.id,
           'image': self.image,
       }
 
class Project(Base):
    """Defines class Project"""
    __tablename__ = 'project'

    #Define colums
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    abstract = Column(String(250))
    description = Column(String(12500))
    image = Column(String(250))
    license = Column(String(16))
    website = Column(String(64))
    category_id = Column(String, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'abstract': self.abstract,
           'description': self.description,
           'image': self.image,
           'license': self.license,
           'website': self.website,
           'category_id': self.category_id,
       }





engine = create_engine('sqlite:///projects_catalog_users.db')
Base.metadata.create_all(engine)

print("Database setup done!")
