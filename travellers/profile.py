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

class ProfileHandler(common.RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('GET')
	def get(self):
		

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		pass
