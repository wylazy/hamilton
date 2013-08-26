#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from HTMLParser import HTMLParser

"""
获取HTML的纯文本
"""
def get_text(html) :
  parse = HTMLParser()

  html = html.strip().strip('\n')
  result = []
  parse.handle_data = result.append

  parse.feed(html)
  parse.close()

  return "".join(result)

"""
去掉HTML标签中的背景颜色
"""
def purge_background(html) :
  pattern = re.compile(r'background-color[^;]*;')
  return pattern.sub('', html)

"""
获取文章摘要，文章摘要通过标签<span abstract></span>来标识
"""
def get_article_abs(html) :
  pattern = re.compile(r'<span[^>]* abstract')
  m = re.search(pattern, html)
  if m :
    return html[:m.start()]
  else :
    print 'Not Match'
    return html

