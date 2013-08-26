#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
from flask import Blueprint, render_template, abort, session, url_for, redirect, request, jsonify
from jinja2 import TemplateNotFound

from bae.api import logging

from database.database import db_session
from dao import dao
from model.user import User
from model.comment import Comment
from model.article import Article
from utils import htmlHelper
from utils import bcsHelper

admin = Blueprint('admin', __name__, template_folder='/templates')

"""
管理员主页面
"""
@admin.route('/')
def index() :

  userid = session.get('userid')
  if not userid :
    return redirect(url_for('.login'))

  try :
    user = User.query.filter(User.id == userid).first()
    if user :
      return render_template('admin/index.html', name=user)
  except TemplateNotFound :
    pass 

  abort(404)

"""
登录页面
"""
@admin.route('/login', methods=['GET', 'POST'])
def login() :
  if session.get('username') :
    return redirect(url_for('.index'))

  username = request.form.get('username')
  password = request.form.get('password')

  if not username or not password :
    if not username :
      username = ''
    return render_template('admin/login.html', username=username)

  ## 验证用户是否合法
  user = User.validate(username, password)

  if user :
    session['userid'] = user.id
    session['username'] = user.name

    redirectUrl = request.args.get('redirectUrl')
    if not redirectUrl :
      redirectUrl = '/'
    return redirect(redirectUrl)


  return render_template('admin/login.html', username=username)

"""
注销界面
"""
@admin.route('/logout')
def logout() :
  session.clear()
  return redirect(url_for('.login'))


"""
获取标签列表, 如果符合当前article，则标记为checked
"""
def get_article_taglist(article_id) :
  tag_chk_list = []
  tag_list = dao.get_all_tags()
  article_ids =  []
  
  if article_id :
    article_ids = dao.get_article_tagids(article_id)
    
  for tag in tag_list :
    chk = {}
    chk['id'] = tag.id
    chk['name'] = tag.name
    chk['checked'] = 'checked' if tag.id in article_ids else ''
    tag_chk_list.append(chk)
  return tag_chk_list

"""
发布一篇博客
"""
@admin.route('/publish', methods=['GET', 'POST'])
def publish() :
  userid = session.get('userid')
  username = session.get('username')

  if not userid or not username:
    return redirect(url_for('admin.login'))

  title = request.form.get('title')
  content = request.form.get('content')

  if not title or not content :
    tag_chk_list = get_article_taglist(0)
    return render_template('admin/publish.html', active = 'publish', article = None, tag_list = tag_chk_list)

  ## 去掉HTML的背景颜色，防止和现有CSS的背景颜色冲突
  content = htmlHelper.purge_background(content)

  ## 向数据库添加一篇文章
  article = Article(userid, username, title, content) 
  db_session.add(article)
  db_session.flush();

  ## 向数据库添加文章标签
  tag_list = request.form.getlist('tags')
  dao.save_tags(article.id, tag_list)
  return redirect('/detail?articleId=%d' % article.id)

"""
编辑博客
"""
@admin.route('/edit', methods=['GET', 'POST'])
def edit() :
  userid = session.get('userid')
  username = session.get('username')

  if not userid or not username:
    return redirect(url_for('admin.login'))

  article_id = int(request.args.get('articleId', 0))

  if not article_id :
    return abort(404)

  ## 从数据库取出博客内容
  article = db_session.query(Article).filter(Article.id == article_id).first()

  if not article :
    return abort(404)

  title = request.form.get('title')
  content = request.form.get('content')
  
  ## 浏览器发送的表单里没有数据，则把编辑页面发送给用户
  if not title or not content :
    tag_list = get_article_taglist(article_id)
    return render_template('admin/publish.html', active = 'publish', article=article, tag_list = tag_list)

  ## 表单里有数据，需要更新数据库
  article.title = title
  article.content = htmlHelper.purge_background(content)
  db_session.flush()

  ## 更新文章的标签表
  tag_list = request.form.getlist('tags')
  dao.update_tags(article_id, tag_list)
  return redirect('/detail?articleId=%d' % article_id)

"""
上传文件，配合UEditor使用
"""
@admin.route('/upload', methods=['POST'])
def upload() :

  userid = session.get('userid')

  if not userid :
    return redirect(url_for('admin.login'))


  file = request.files['upfile']
  if not file :
    return abort(404)
  
  ### BAE不支持文件存储，所以要将上传的文件存储到BCS
  url = bcsHelper.transfer_file(file)

  """ 
     * 这是Ueditor所接收的数据格式, 向浏览器返回数据json数据
     * {
     *   'url'      :'a.jpg',   //保存后的文件路径
     *   'title'    :'hello',   //文件描述，对图片来说在前端会添加到title属性上
     *   'original' :'b.jpg',   //原始文件名
     *   'state'    :'SUCCESS'  //上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
     * }
     */
  """
  if url :
    return jsonify(url = url, title='', original = file.filename, state='SUCCESS')
  else :
    return jsonify(url = '', title='', original = file.filename, state='FAILED')
