#!/usr/bin/env python
# coding=utf-8

# Jack Kang
import json
from kazoo.client import KazooClient

zk = KazooClient("123.206.89.123:2181")
zk.start()
list = zk.get_children("/task/taobao/node-0000000495")
for task in list:
    data,stat = zk.get("/task/taobao/node-0000000495/" + task)
    print data
zk.stop()
