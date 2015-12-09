#!/usr/bin/python

import sys, os, threading, base64
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

class AvatarHandler(common.RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('GET')
	def get(self):
		id_ = None
		if self.request.arguments.has_key('id'):
			id_ = self.get_argument('id')
		if id_ is None or len(id_) == 0:
			self.exception_handle('Missing argument \'id\'')
			return
		avatar = yield MySQLHelper.fetch_avatar(id_)
		if avatar is None or len(avatar) == 0:
			self.exception_handle('Specific avatar not found')
			return
		try:
			avatar = base64.b64decode(avatar)
		except Exception, e:
			self.exception_handle('Base64 decoding failure')
			return
		self.set_header('Content-Type', 'image/*')
		self.write(avatar)
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
		avatar = self.body_json_object.get('avatar')
		if avatar is None or len(avatar) == 0:
			self.exception_handle(
				'Missing argument \'avatar\'')
			return
		rc = yield MySQLHelper.modify_avatar(uid, avatar)
		if rc is None or rc == 0:
			self.exception_handle('The database operation failed (MySQL.ModifyAvatar)')
			return
		self.write(self.gen_result(0, 'Successfully changed', 'ok'))


