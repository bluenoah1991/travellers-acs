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

class ForgetHandler(common.RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		tel = self.body_json_object.get('tel')
		if tel is None or len(tel) == 0:
			self.exception_handle('Missing argument \'tel\'')
			return
                if not re.match(r'^[1][0-9]{10}$', tel):
                        self.exception_handle('\'tel\' format is not correct')
                        return
		request_password = self.body_json_object.get('password')
		if request_password is None or len(request_password) == 0:
			self.exception_handle('Missing argument \'password\'')
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
		try:
			rc = MySQLHelper.modify_password_by_tel(tel, request_password)
		except Exception, e:
			self.exception_handle('Password change failed (MySQL)')
		if rc is None or rc == 0:
			self.exception_handle('Password change failed (MySQL)')
			return
		self.write(self.gen_result(0, 'Successfully changed', 'ok'))


