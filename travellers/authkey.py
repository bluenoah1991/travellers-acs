#!/usr/bin/python

import sys, os, threading
import tornado.web
import tornado.gen
import logging
import random

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config
from db import MySQLHelper

logger = logging.getLogger('web')

class AuthKeyHandler(common.RequestHandler):

	@tornado.gen.coroutine
	def post(self):
		code = random.randint(100000, 999999)
		# redis queue
		

