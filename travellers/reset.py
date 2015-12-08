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

class ResetHandler(common.RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(
				'Session timeout')
			return
		request_password = self.body_json_object.get('password')
		if request_password is None or len(request_password):
			self.exception_handle('Missing argument \'password\'')
			return
		# TODO Check password format
		try:
			rc = MySQLHelper.modify_password(uid, request_password)
		except Exception, e:
			self.exception_handle('Password change failed (MySQL)')
			return
		if rc is None or rc == 0:
			self.exception_handle('Password change failed (MySQL)')
			return
		self.session_rm()
		self.write(self.gen_result(0, 'Successfully changed', 'ok'))

