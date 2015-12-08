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

class RegisterHandler(common.RequestHandler):

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
		password = self.body_json_object.get('password')
		if password is None or len(password) == 0:
			self.exception_handle('Missing argument \'password\'')
			return
		# TODO Check password format
		deviceid = self.body_json_object.get('deviceid')
		if deviceid is None or len(deviceid) == 0:
			self.exception_handle('Missing argument \'deviceid\'')
			return
		if not re.match(r'^[1][0-9]{10}$', tel):
			self.exception_handle('\'tel\' format is not correct')
			return
		code = self.body_json_object.get('code')
		if code is None or len(code) == 0:
			self.exception_handle('Missing argument \'code\'')
			return
		if len(code) <> 6:
			self.exception_handle('Auth code format exception, %s' % code)
			return
		r = common.get_redis_0()
		if r is None:
			self.exception_handle('Invalid Redis connection')
			return
		xcode = None
		try:
			xcode = r.get(tel)
		except Exception, e:
			self.exception_handle('The database operation failed (Redis.Get)')
			return
		if xcode is None or xcode <> code:
			self.exception_handle(
				'The phone or pin you entered was incorrect. Please try again')
			return
		id_ = yield MySQLHelper.add_user(self.body_json_object)
		if id_ is None:
			self.exception_handle('The database operation failed (MySQL.AddUser)')
			return
		self.body_json_object.id = id_
		self.write(self.gen_result(0, 'Registered success', self.body_json_object))
		return

