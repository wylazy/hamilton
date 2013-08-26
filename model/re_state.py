#!/usr/bin/env python
#-*- coding:utf-8 -*-

class ReState :

  def __init__(self, state, message) :
    self.state = True if state else False
    self.message = message
