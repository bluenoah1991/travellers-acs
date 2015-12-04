#!/usr/bin/python

import sys, os
import json
import tornado.web
import logging

reload(sys)
sys.setdefaultencoding('utf8')

import config

logger = logging.getLogger('web')

def get_file_from_current_dir(_file_, filename):
	path = os.path.split(os.path.realpath(_file_))[0]
	return os.path.join(path, filename)

def pretty_print(jsonstr):
	if jsonstr is None or len(jsonstr) == 0:
		return jsonstr
	prettystr = '<html><body><pre><code>\r\n'
	try:
		obj = json.loads(jsonstr)
		prettystr += json.dumps(obj, indent=4, sort_keys=True)
	except Exception, e:
		logger.error('JSON parse failure (Pretty Print)')
		return jsonstr
	prettystr += '\r\n'
	prettystr += '</code></pre></body></html>'
	prettystr = prettystr.decode('unicode_escape')
	return prettystr

def strict_str(str_):
	str_ = str_.replace('"', '\\"')
	str_ = str_.strip()
	return str_

class RequestHandler(tornado.web.RequestHandler):

	def write(self, trunk):
		if type(trunk) == int:
			trunk = str(trunk)
		super(RequestHandler, self).write(trunk)

	def get(self, *args, **kwargs):
		if config.Mode == 'DEBUG':
			logger.debug('Request URI: %s (%s)(GET)' % (self.request.uri, self.request.remote_ip))
		super(RequestHandler, self).get(self, args, kwargs)

	def post(self, *args, **kwargs):
		if config.Mode == 'DEBUG':
			logger.debug('Request URI: %s (%s)(POST)' % (self.request.uri, self.request.remote_ip))
		super(RequestHandler, self).post(self, args, kwargs)


