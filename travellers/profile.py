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

class ProfileHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('GET')
	def get(self):
		id_ = None
		session_id_ = self.session_get()
		if self.request.arguments.has_key('id'):
			id_ = self.get_argument('id')
		if id_ is None or len(id_) == 0:
			id_ = session_id_
		if id_ is None or len(id_) == 0:
			self.exception_handle('Missing argument \'id\'')
			return
		user = None
		if id_ <> session_id_:
			user = yield MySQLHelper.fetch_base_profile(id_)
		else:
			user = yield MySQLHelper.fetch_profile(id_)
		if user is None:
			self.exception_handle('User not found')
			return
		self.write(self.gen_result(0, 'Account profile', user))
		return

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(
				'Session timeout')
			return
		if self.body_json_object is None:
			self.exception_handle(
				'Request data format exception, %s' % self.request.uri)
			return
		self.body_json_object['id'] = uid
		rc = yield MySQLHelper.update_profile(self.body_json_object)
		if rc is None or rc == 0:
			self.exception_handle('The database operation failed (MySQL.UpdateProfile)')
			return
		self.write(self.gen_result(0, 'Successfully changed', 'ok'))


