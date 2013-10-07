#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bae.core import const
from flask import Blueprint, render_template, abort, session, url_for, redirect, request, jsonify
from database.database import db_session
from utils import social
from model.user import User

oauth = Blueprint('oauth', __name__, template_folder='/templates')

@oauth.route('/callback')
def callback() :
  code = request.args.get('code', None)

  if code :
    token = social.get_access_token(code)
    access_token = token.get('access_token')

    if access_token :
      baidu_user = social.get_user_info(access_token)
      name = baidu_user.get('username')
      media_type = baidu_user.get('media_type')
      head_url = baidu_user.get('tinyurl')
      
      user = User.find_user(name, media_type)
      if not user and name :
        user = User(name, head_url = head_url, media_type = media_type)
        db_session.add(user)
        db_session.flush();

      if user :
        session['userid'] = user.id
        session['username'] = user.name
        session['is_admin'] = user.admin

  return redirect('/') 
