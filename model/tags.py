#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_, not_
from database.database import Base

class Tags(Base) :

  __tablename__ = 'TAGS'

  id = Column(Integer, primary_key=True)
  name = Column(String(16), unique=True)

  def __init__(self, id, name) :
    self.id = id
    self.name = name

