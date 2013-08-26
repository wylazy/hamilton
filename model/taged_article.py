#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_, or_, not_
from database.database import Base

class TagedArticle(Base) :

  __tablename__ = 'TARGED_ARTICLE'

  id = Column(Integer, primary_key=True)
  tag_id = Column(Integer, primary_key=True)
  article_id = Column(Integer, primary_key=True)
  tag_name = Column(String(16), unique=True)

  def __init__(self, tag_id, article_id, tag_name) :
    self.tag_id = tag_id
    self.article_id = article_id
    self.tag_name = tag_name
