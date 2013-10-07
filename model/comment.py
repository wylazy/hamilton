#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_, not_
from database.database import Base

class Comment(Base) :

  __tablename__ = 'COMMENTS'

  id = Column(Integer, primary_key=True)
  article_id = Column(Integer)
  user_id = Column(Integer)
  user_name = Column(String(16))
  user_url = Column(String(255))
  to_name = Column(String(16))
  content = Column(String(280))

  def __init__(self, article_id, user_id, user_name, user_url, to_name, content) :
    self.article_id = article_id
    self.user_id = user_id
    self.user_name = user_name
    self.user_url = user_url
    self.to_name = to_name
    self.content = content
