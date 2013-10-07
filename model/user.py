#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_, not_
from database.database import Base

class User(Base) :

  __tablename__ = 'USER'

  id = Column(Integer, primary_key=True)
  name = Column(String(16), unique=True)
  email = Column(String(24), unique=True)
  passwd = Column(String(40))
  head_url = Column(String(255))
  admin = Column(Integer)
  media_type = Column(String(40))
  token = Column(String(40))
  auth_time = Column(DateTime)

  def __init__(self, name, email = None, passwd = '', head_url = '', admin = 0, media_type = '', token = '') :
    self.name = name
    self.email = email
    self.passwd = passwd
    self.head_url = head_url
    self.admin = admin
    self.media_type = media_type
    self.token = token

  @staticmethod
  def validate(name, passwd) :

    if name and passwd :

      ## search by username
      user = User.query.filter(and_(User.name == name, User.passwd == passwd)).first() 
      if user :
        return user
      
      ## search by email
      user = User.query.filter(and_(User.email == name, User.passwd == passwd)).first()
      if user :
        return user

    return None

  @staticmethod
  def find_user(name, media_type) :
    if name :
      user = User.query.filter(and_(User.name == name, User.media_type == media_type)).first()
      if user :
        return user

    return None
