#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_, not_
from database.database import Base

class Article(Base) :

  __tablename__ = 'ARTICLE'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer)
  user_name = Column(String(16))
  title = Column(String(64))
  content = Column(String(65535))
  update_time = Column(DateTime)

  def __init__(self, userid, username, title, content) :
    self.user_id = userid
    self.user_name = username
    self.title = title
    self.content = content
    self.text = ''
