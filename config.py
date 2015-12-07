#!/usr/bin/python

import os

VERSION = '0.0.1'

Mode = 'DEBUG'
#Mode = 'RELEASE'

## MySQL Configuration

MySQL_Unix_Socket = '/var/run/mysqld/mysqld.sock'
MySQL_User = 'root'
MySQL_Passwd = '123456'
MySQL_DB = 'travellers'

## Redis Configuration

Redis_Unix_Socket = '/var/run/redis/redis-6379.sock'

AuthCode_ExpireTime = 60 * 60 * 10
