#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import and_, or_, not_, func, desc
from bae.api import logging

from database.database import db_session
from model.user import User
from model.tags import Tags
from model.comment import Comment
from model.taged_article import TagedArticle
from model.tag_aggr import TagAggr
from model.article import Article

"""
查询全部标签
"""
def get_all_tags() :
  return db_session.query(Tags).all()

"""
查询某个标签下的全部文章
"""
def get_taged_articles(tag_id) :
   return db_session.query(Article).join(TagedArticle, TagedArticle.article_id == Article.id).filter(TagedArticle.tag_id == tag_id).order_by(Article.id).all()

"""
查询全部标签，以及这个标签下有多少文章
"""
def aggregate_taged_article() :

  tag_list = []
  tmp_list = db_session.query(TagedArticle.tag_id, TagedArticle.tag_name, func.count(TagedArticle.tag_id).label('count')).group_by(TagedArticle.tag_id, TagedArticle.tag_name).order_by(desc('count')).all()

  for tup in tmp_list :
    tag_list.append(TagAggr(tup[0], tup[1], tup[2]))

  return tag_list

"""
查询某个文章所属的标签列表
"""
def get_article_tags(article_id) :
  tag_list = []
  v_list = db_session.query(TagedArticle.tag_id, TagedArticle.tag_name).filter(TagedArticle.article_id == article_id).all()
  for v in v_list :
    tag_list.append(Tags(v[0], v[1]))
  return tag_list

"""
查询某个文章所属的标签id列表
"""
def get_article_tagids(article_id) :
  tag_ids = []
  v_list = db_session.query(TagedArticle.tag_id).filter(TagedArticle.article_id == article_id).all()
  for v in v_list :
    tag_ids.append(v[0])
  return tag_ids

"""
保存文章对应的标签
"""
def save_tags(article_id, tag_list) :

  if not tag_list :
    return None

  for tag_id in tag_list :
    tag_name = db_session.query(Tags.name).filter(Tags.id == tag_id).first()[0]
    db_session.add(TagedArticle(tag_id, article_id, tag_name))
  db_session.flush()

"""
将文章现有的标签更改为tag_list
"""
def update_tags(article_id, tag_list) :
  db_session.query(TagedArticle).filter(TagedArticle.article_id == article_id).delete()
  save_tags(article_id, tag_list)

"""
获取文章的评论，暂不支持分页
"""
def get_article_comments(article_id) :
  return db_session.query(Comment).filter(Comment.article_id == article_id).order_by(desc(Comment.id)).all()
