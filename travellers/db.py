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
		try:
			yield pool.execute(sql_statement, (id_ , password_, name_, tel_, email_, deviceid_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
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
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (new_password, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)
	
	@classmethod
	@tornado.gen.coroutine
	def modify_password_by_tel(cls, tel, new_password):
		if tel is None:
			logger.error('Missing argument \'tel\'')
			raise tornado.gen.Return(None)
		if new_password is None or len(new_password) == 0:
			logger.error('Missing argument \'password\'')
			raise tornado.gen.Return(None)
		sql_statement = ('UPDATE `users` SET '
				'`password` = %s'
				' WHERE '
				'`tel` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (new_password, tel))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
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
				'`name` = %s, '
				'`tel` = %s, '
				'`email` = %s, '
				'`deviceid` = %s'
				' WHERE '
				'`id` = %s')
		cur = None
		try:
			cur = yield pool.execute(sql_statement, 
				(name_, tel_, email_, deviceid_, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
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
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def fetch_avatar(cls, id_):
		if id_ is None:
			logger.error('Missing argument \'id\'')
			raise tornado.gen.Return(None)
		sql_statement = 'SELECT `avatar` FROM `users` WHERE `id` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		if profile is None:
			logger.error('Specific row not found')
			raise tornado.gen.Return(None)
		avatar = profile.get('avatar')
		raise tornado.gen.Return(avatar)
		
	@classmethod
	@tornado.gen.coroutine
	def modify_avatar(cls, id_, avatar_base64string):
		if id_ is None:
			logger.error('Missing argument \'id\'')
			raise tornado.gen.Return(None)
		if avatar_base64string is None or len(avatar_base64string) == 0:
			logger.error('Missing argument \'avatar_base64string\'')
			raise tornado.gen.Return(None)
		sql_statement = ('UPDATE `users` SET '
				'`avatar` = %s'
				' WHERE '
				'`id` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (avatar_base64string, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)

	@classmethod
	@tornado.gen.coroutine
	def fetch_base_profile(cls, id_):
		if id_ is None:
			logger.error('Missing argument \'id\'')
			raise tornado.gen.Return(None)
		sql_statement = ('SELECT '
			'`id`, `name`, `avatar`, `email`'
			' FROM `users` WHERE `id` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def fetch_profile_by_tel(cls, tel):
		if tel is None:
			logger.error('Missing argument \'tel\'')
			raise tornado.gen.Return(None)
		sql_statement = 'SELECT * FROM `users` WHERE `tel` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (tel,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)
		

