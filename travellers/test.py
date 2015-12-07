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
from db import MySQLHelper

logger = logging.getLogger('web')

class TestHandler(common.RequestHandler):

	@tornado.gen.coroutine
	def get(self):
		self.write(111)
		import pdb
		pdb.set_trace()
		#a = yield MySQLHelper.add_user({
		#		'name': 'test1',
		#		'password': 'QWERTYUIasdfghj'
		#	})
		a = yield MySQLHelper.modify_password('bfb7c38a-9bda-11e5-8ad1-5254001a7787', '123456')
		pdb.set_trace()
		self.write(222)

