#!/usr/bin/env python
# coding=utf-8

# Jack Kang
from kazoo.client import KazooClient
#import kazoo
import logging
logging.basicConfig()
zk = KazooClient(hosts = '192.168.30.170:2181')
zk.start()
if zk.exists("/zkang"):
    print "Ok"
else:
    print "NO"
zk.stop()
