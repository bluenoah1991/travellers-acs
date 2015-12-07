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
		if user is None:
			logger.error('Missing field \'user\'')
			raise tornado.gen.Return(None)
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
		pool = common.get_mysql_pool()
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
		sql_statement = ('UPDATE `users` SET '
				'`password` = %s'
				' WHERE '
				'`id` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = yield pool.execute(sql_statement, (new_password, id_))
		raise tornado.gen.Return(cur.rowcount)
	
	@classmethod
	@tornado.gen.coroutine
	def update_profile(cls, profile):# TODO Avatar
		if profile is None:
			logger.error('Missing argument \'profile\'')
			raise tornado.gen.Return(None)
		id_ = profile.get('id')
		if id_ is None:
			logger.error('Missing argument \'id\'')
			raise tornado.gen.Return(None)
		sql_statement = 'SELECT * FROM `users` WHERE `id` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = yield pool.execute(sql_statement, (id_,))
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		raw_user = cur.fetchone()
		name_ = profile.get('name', raw_user.get('name'))
		tel_ = profile.get('tel', raw_user.get('tel'))
		email_ = profile.get('email', raw_user.get('email'))
		deviceid_ = profile.get('deviceid', raw_user.get('deviceid'))
		sql_statement = ('UPDATE `users` SET '
				'`name` = %s '
				'`tel` = %s '
				'`email` = %s '
				'`deviceid` = %s'
				' WHERE '
				'`id` = %s')
		cur = yield pool.execute(sql_statement, 
				(name_, tel_, email_, deviceid_, id_))
		raise tornado.gen.Return(cur.rowcount)

	@classmethod
	@tornado.gen.coroutine
	def fetch_profile(cls, id_):
		if id_ is None:
			logger.error('Missing argument \'id\'')
			raise tornado.gen.Return(None)
		sql_statement = 'SELECT * FROM `users` WHERE `id` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = yield pool.execute(sql_statement, (id_,))
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)
		

