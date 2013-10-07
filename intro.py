#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, abort, session, url_for, redirect, request, jsonify
from jinja2 import TemplateNotFound
from sqlalchemy import and_, or_, not_, desc

from bae.api import logging

from database.database import db_session
from dao import dao
from model.paging import Paging
from model.paging import PAGE_SIZE
from model.user import User
from model.tags import Tags
from model.comment import Comment
from model.re_state import ReState
from model.taged_article import TagedArticle
from model.tag_aggr import TagAggr
from model.article import Article
from utils import htmlHelper
from utils import bmq

intro = Blueprint('intro', __name__, template_folder='/templates')


"""
首页
"""
@intro.route('')
def index() :

  page = int(request.args.get('page', 1))

  ## 获取最新的文章
  record_size = db_session.query(Article).count()
  article_list = db_session.query(Article).filter(Article.title != '').order_by(desc(Article.id)).offset(PAGE_SIZE*(page-1)).limit(PAGE_SIZE)

  paging = Paging(page, record_size, request.args)

  ## 侧边栏显示的标签
  tag_list = dao.aggregate_taged_article()

  ## 提取文章的摘要部分
  article_dic = {}
  for article in article_list :
    article_dic[article.id] = htmlHelper.get_article_abs(article.content)

  return render_template('index.html', active='home', tag_list = tag_list, article_list = article_list, article_dic = article_dic, paging = paging)

"""
获取标签下的文章
"""
@intro.route('tags')
def tags() :
  page = int(request.args.get('page', 1))
  tag_id = int(request.args.get('tagid'))
  if not tag_id :
    return abort(404)

  tag_name = db_session.query(Tags.name).filter(Tags.id == tag_id).first()[0]

  ## 侧边栏显示的标签
  tag_list = dao.aggregate_taged_article()

  ## 查询标签tag_id下的全部文章，并提取摘要部分
  record_size, article_list = dao.get_taged_articles(tag_id, (page-1)*PAGE_SIZE)
  paging = Paging(page, record_size, request.args)

  article_dic = {}
  for article in article_list :
    article_dic[article.id] = htmlHelper.get_article_abs(article.content)

  return render_template('tags.html', active='home', tag_list = tag_list, tag_name = tag_name, article_list = article_list, article_dic = article_dic, paging = paging)
  
"""
获取文章的内容
"""
@intro.route('detail')
def detail() :
  article_id = int(request.args.get('articleId', 0))

  if not article_id :
    abort(404)

  article = db_session.query(Article).filter(Article.id == article_id).first()

  if not article :
    return abort(404)

  ## 获取文章所属的标签
  tag_list = dao.get_article_tags(article_id)

  ## 获取文章的全部评论
  comments = dao.get_article_comments(article_id)
  return render_template('article.html', active='home', article = article, tag_list = tag_list, comments=comments)

"""
添加一条评论
"""
@intro.route('comment', methods=['GET', 'POST'])
def comment() :
  article_id = request.form.get('articleId') or 0

  if not article_id :
    return jsonify(state=False, message='文章不存在')

  user_id = session.get('userid')
  user_name = session.get('username')
  to_name = request.form.get('toName') or None
  content = request.form.get('content') or None

  if not content :
    return jsonify(state=False, message='评论内容不能为空')
 
  if not user_name or not user_id :
    return jsonify(state=False, message='用户未登录')

  user = db_session.query(User).filter(User.id == user_id).first()
  ## 向数据库添加一条评论
  c = Comment(article_id, user.id, user.name, user.head_url, to_name, content)
  db_session.add(c)
  db_session.flush()

  article_url = 'http://hamilton.duapp.com/detail?articleId=' + str(article_id)
  bmq.send_mail(['wangyulong_1214@qq.com'], 'hamilton上的新回复', '<!--HTML-->\n您有一条新回复需要处理<br/>点击查看：<a href="' + article_url + '">' + article_url + '</a>')

  return jsonify(state=True, message='success')

"""
说明界面
"""
@intro.route('about')
def about() :
  #logging.debug('access about')
  return render_template('about.html', active="about")

"""
联系我
"""
@intro.route('contact')
def contact() :
  return render_template('contact.html', active="contact")

@intro.route('favicon.ico')
def favicon() :
  return redirect(url_for('static', filename='img/favicon.ico'))

