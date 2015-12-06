#!/usr/bin/python

import sys, os, uuid
import logging
import tornado.gen

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config

logger = logging.getLogger('web')

class MySQLHelper:

	@classmethod
	@tornado.gen.coroutine
	def add_user(cls, user):
		import pdb
		pdb.set_trace()
		id_ = user.get('id', str(uuid.uuid1()))
		password_ = user.get('password')
		if password_ is None or len(password_) == 0:
			logger.error('Missing field \'password\'')
			raise tornado.gen.Return(None)
		name_ = user.get('name', '')
		tel_ = user.get('tel', '')
		email_ = user.get('email', '')
		deviceid_ = user.get('deviceid', '')
		sql_statement = ('INSERT INTO `users` '
				'(`id`, `password`, `name`, `tel`, `email`, `deviceid`)'
				' VALUES '
				'(%s, %s, %s, %s, %s, %s)')
		pool = common.get_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		yield pool.execute(sql_statement, (id_ , password_, name_, tel_, email_, deviceid_))
		raise tornado.gen.Return(id_)


	@classmethod
	@tornado.gen.coroutine
	def modify_password(cls, id_, new_password):
		if id_ is None:
			logger.error('Missing argument \'id\'')
			raise tornado.gen.Return(None)
		if new_password is None or len(new_password) == 0:
			logger.error('Missing argument \'password\'')
			raise tornado.gen.Return(None)

























		
