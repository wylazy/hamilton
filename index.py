#!/usr/bin/env python
#-*- coding:utf-8 -*-


from flask import Flask, g, request, render_template

from bae.core.wsgi import WSGIApplication
from bae.api import bcs

from admin.admin import admin
from intro import intro
from database.database import init_db, db_session

 

init_db()

app = Flask(__name__)
app.debug = True
app.secret_key = 'b8Ge798&32hLiPA /*z!~/ogiu921'

app.register_blueprint(intro, url_prefix = '/')
app.register_blueprint(admin, url_prefix = '/admin')

application = WSGIApplication(app)


#@app.teardown_appcontext
#def shutdown_session(exception=None):
#  db_session.remove()
