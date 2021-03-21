from sqlalchemy import  Column, Integer, String,DateTime,ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
import datetime
#from courses_live.database import Base1
from app.talent.database import Base
#from app.All_Course.models import Course
class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True,unique=True)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    username = Column(String,unique=True)
    email = Column(String,unique=True)
    password = Column(String)
    confirm_password = Column(String)
    dateofbirth = Column(String)
    phone = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    status = Column(String)
    passcode = Column(Integer)
    is_admin = Column(String)
    paid = relationship('Paid',back_populates='client')
    paid3 = relationship('Payment',back_populates='clients')
    user_wish = relationship('Wishlist', back_populates='users_wish')
    user_pro = relationship('Project', back_populates='project_id')
    user_notes = relationship('Notes', back_populates='notes_id')
    
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    title = Column(String)
    name = Column(String)
    price = Column(Integer)
    desc = Column(String)
    type = Column(String)
    status = Column(Integer)
    paid1 = relationship('Paid',back_populates='course')
    paid2 = relationship('Payment',back_populates='courses')
    course_comment = relationship('Comment', back_populates='course_related')
    user_course = relationship('Wishlist',back_populates='course_wish')
class Paid(Base):
    __tablename__ = "paids"
    id = Column(String, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    name = Column(String)
    #amount = Column(Integer)
    client_id = Column(String, ForeignKey('users.id'))
    client = relationship('Users', back_populates='paid')
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='paid1')
    
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    is_active = Column(Boolean,default=True)
    name = Column(String)
    Message = Column(String)
    courses_id = Column(Integer, ForeignKey('courses.id'))

    course_related = relationship('Course',back_populates='course_comment')

class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    client_id = Column(String, ForeignKey('users.id'))
    users_wish = relationship('Users', back_populates='user_wish')
    course_id = Column(Integer, ForeignKey('courses.id'))
    course_wish = relationship('Course', back_populates='user_course')

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    first_name = Column(String)
    details = Column(String)
    client_id = Column(String, ForeignKey('users.id'))
    project_id = relationship('Users', back_populates='user_pro')

class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    detail = Column(String)
    client_id = Column(String, ForeignKey('users.id'))
    notes_id = relationship('Users', back_populates='user_notes')