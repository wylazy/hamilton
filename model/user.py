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
  token = Column(String(40))
  auth_time = Column(DateTime)


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
