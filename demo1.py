#!/usr/bin/env python
# coding=utf-8

# Jack Kang
from kazoo.client import KazooClient
import logging
import time
import sys

def doSlaveWork(zk):
    @zk.ChildrenWatch("/task")
    def watch_children(children):
        print "task now is %s" % children
    id = 0
    while True:
        task = "/task/" + str(id)
        data, stat = zk.get(task)
        print "data%s" % data.decode("utf-8")
        id += 1
        #print id
        time.sleep(3)
        if True == judgeStopFlag(zk) :
            sys.exit()
    
def doMasterWork(zk,):
    id = 0
    while True:
        task = "/task/" + str(id)
        value = "csdn" + str(id)
        print task
        zk.create(task,value)
        id += 1
        time.sleep(1)
        if judgeStopFlag(zk) == True:
            zk.stop()
            sys.exit()

def judgeStopFlag(zk):
    if zk.exists("/stop"):
        zk.stop()
        return True
    else:
        return False

def myWatch(event):
    print "event"



zk = KazooClient(hosts = '192.168.30.132:2181');
zk.start()

@zk.add_listener
def my_listener(state):
    if state == KazooState.LOST:
        print("LOST")
    elif state == KazooState.SUSPENDED:
        print("SUSPENDED")
    else:
        print("Connected")

while True:
    if zk.exists("/master",watch=myWatch):
        print "master is alive"
        doSlaveWork(zk)
    else:
        zk.create("/master",ephemeral = True)
        print "I am the master"
        doMasterWork(zk)

    judgeStopFlag(zk)

zk.stop()
