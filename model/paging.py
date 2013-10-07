#!/usr/bin/env python
#-*- coding:utf-8 -*-

PAGE_SIZE = 10

class Paging :

  def __init__(self, page, size, args) :
    self.cur_page = page
    self.min_page = max(1, page-4)
    self.max_page = min(page+4, (size - 1)/PAGE_SIZE + 1)

    self.args = '';
    for key, value in args.iteritems() :
      if cmp('page', key.lower()) :
        self.args += '&' + key + '=' + value


