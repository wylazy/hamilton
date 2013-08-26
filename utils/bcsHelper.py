#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import os
from bae.core import const
from bae.api import bcs

from database.database import db_session
from model.comment import Comment


HOST = const.BCS_ADDR
AK = const.ACCESS_KEY
SK = const.SECRET_KEY
APP_TMPDIR = const.APP_TMPDIR

BUCKET = 'hamilton-000000'
BCS_PATH = '/resources/'
SCHEMA = 'http://'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_filename(filename) :
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
将上传的文件存到BCS，并返回BCS的URL
"""
def transfer_file(flask_file) :

  filename = flask_file.filename
  filename = filename[filename.rfind('/')+1:]

  if not filename or not allowed_filename(filename) :
    return None

  baebcs = bcs.BaeBCS(HOST, AK, SK)

  remote_name = str(BCS_PATH + str(time.time()) + '.' + filename)
  filedata = flask_file.read()

  ## 上传到BCS
  baebcs.put_object(BUCKET, remote_name, filedata) 

  return SCHEMA + HOST + '/' + BUCKET + remote_name
