#!/usr/bin/env python
# coding=utf-8

# Jack Kang
from kazoo.client import KazooClient
import logging 
import time

logging.basicConfig()

zk = KazooClient(hosts = "192.168.30.132:2181")
zk.start()
if zk.exists("/task/"):
    zk.delete("/task",recursive = True)
    print "delete task success"
    zk.create('/task')
else:
    print "no delete"

if zk.exists("/stop"):
    zk.delete("/stop")
    print "delete stop success"
if zk.exists("/master"):
    zk.delete("/stop")

zk.stop()

