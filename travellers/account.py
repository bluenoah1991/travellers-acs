#!/usr/bin/python

import sys, os, threading
import tornado.web
import tornado.gen
import logging

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config

logger = logging.getLogger('web')

class AccountHandler(tornado.web.RequestHandler):

	@tornado.gen.coroutine
	def get(self):
		pass

	def write(self, trunk):
		if type(trunk) == int:
			trunk = str(trunk)
		super(AccountHandler, self).write(trunk)

