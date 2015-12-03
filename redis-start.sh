#!/bin/bash

apt-get install redis-server -y
/etc/init.d/redis-server stop

redis-server ./redis-config/6379.conf
echo 'Service 6379 has been started'
redis-server ./redis-config/6380.conf
echo 'Service 6380 has been started'

