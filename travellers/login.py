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
from handler import RequestHandler
from db import MySQLHelper

logger = logging.getLogger('web')

class LoginHandler(RequestHandler):

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
		user = yield MySQLHelper.fetch_profile_by_tel(tel)
		if user is None:
			self.exception_handle('User not found')
			return
		request_password = self.body_json_object.get('password')
		if request_password is None or len(request_password) == 0:
			self.exception_handle('Missing argument \'password\'')
			return
		password = user.get('password', '')
		if request_password <> password:
			self.exception_handle('Incorrect password')
			return
		request_deviceid = self.body_json_object.get('deviceid')
		if request_deviceid is None or len(request_deviceid) == 0:
			self.exception_handle('Missing argument \'deviceid\'')
			return
		deviceid = user.get('deviceid', '')
		if request_deviceid <> deviceid:
			self.exception_handle('Incorrect device id')
			return
		uu = self.session_set(user.get('id'))
		if uu is None or len(uu) == 0:
			self.exception_handle('Session setup failed')
			return
		self.write(self.gen_result(0, 'Successfully login', uu))
		
