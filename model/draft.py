#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_, not_
from database.database import Base

class Draft(Base) :

  __tablename__ = 'DRAFT'

  id = Column(Integer, primary_key=True)
  article_id = Column(Integer)
  user_id = Column(Integer)
  user_name = Column(String(16))
  title = Column(String(64))
  content = Column(String(65535))

  def __init__(self, article_id, userid, username, title, content) :
    self.article_id = article_id
    self.user_id = userid
    self.user_name = username
    self.title = title
    self.content = content
