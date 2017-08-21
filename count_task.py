#!/usr/bin/env python
# coding=utf-8

# Jack Kang
from kazoo.client import KazooClient
zk = KazooClient("123.206.89.123:2181")
zk.start()
zk.create("/signal/taobao/pause")
all_task_dir = zk.get_children("/task/taobao")
for task_dir in all_task_dir:
    task_list = zk.get_children("/task/taobao/" + task_dir)
    print "task_dir: " + task_dir + "   "+ str(len(task_list))
zk.create("/signal/taobao/continue")
zk.stop()
