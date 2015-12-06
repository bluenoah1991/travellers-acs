#!/usr/bin/python

import sys, os, uuid
import logging

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config

logger = logging.getLogger('web')

class MySQLHelper:

	@classmethod	
	def add_user(cls, user):
		id_ = user.get('id', str(uuid.uuid1())
		password_ = user.get('password')
		if password_ is None or len(password_) == 0:
			logger.error('Missing field \'password\'')
			return None
		name_ = user.get('name', '')
		tel_ = user.tel('tel', '')
		email_ = user.tel('email', '')
		deviceid_ = user.tel('deviceid_', '')
		sql_statement = ('INSERT INTO `users` '
				'(`id`, `password`, `name`, `tel`, `email`, `deviceid`)'
				' VALUES '
				'(%s, %s, %s, %s, %s, %s)')
		pool = common.get_pool()
		if pool is None:
			 logger.error('Unknown connection pool')
			 return None
		yield pool.execute(sql_statement, (id_ , password_, name_, tel_, email_, deviceid_))
		return id_

	@classmethod
	def modify_password(cls, id_, new_password):
		if id_ is None:
			logger.error('Missing argument \'id\'')
			return None
		if new_password is None or len(new_password) == 0:
			logger.error('Missing argument \'password\'')
			return None
			
			
