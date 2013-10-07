#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bae.core import const
from bae.api.bcms import BaeBcms

REAL_QNAME = 'd4fae8f666267c8126b2620443e6ecee'

"""
to = ["xxx@lalala.com"]
ret = bcms.mail(real_qname, "你好，我们是BAE", to, "support@baidu.com",
"hello from BAE")

"""
def send_mail(to, subject, content) :
  bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
  return bcms.mail(REAL_QNAME, content, to, 'hamilton@baidu.com', subject)
