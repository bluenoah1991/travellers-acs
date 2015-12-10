#!/usr/bin/python

import sys, os, threading, re
import tornado.web
import tornado.gen
import logging
import random

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config
from handler import RequestHandler
from db import MySQLHelper

logger = logging.getLogger('web')

class AuthKeyHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(
				'Request data format exception, %s' % self.request.uri)
			return
		tel = self.body_json_object.get('tel')
		if tel is None or len(tel) == 0:
			self.exception_handle('Missing argument \'tel\'')
			return
		if not re.match(r'^[1][0-9]{10}$', tel):
			self.exception_handle('\'tel\' format is not correct')
			return
		code = random.randint(100000, 999999)
		# TODO Send SMS message
		print 'your auth code is %s' % code
		r = common.get_redis_0()
		if r is None:
			self.exception_handle('Invalid Redis connection')
			return
		try:
			r.set(tel, code, ex=config.AuthCode_ExpireTime) # Block ?
		except Exception, e:
			self.exception_handle('The database operation failed (Redis.Set)')
			return
		self.write(self.gen_result(0, 'Successfully sent', 'ok'))
		return
