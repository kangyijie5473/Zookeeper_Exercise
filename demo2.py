#!/usr/bin/env python
# coding=utf-8

# Jack Kang
from kazoo.client import KazooClient
import logging
import sys
import time
import random

class Kworker:

    __worker_id = 0
    task_id = 5

    def __init__(self, hosts_list =  ['192.168.30.132:2181', '192.168.30.160:2181', '192.168.30.170:2181'], id = 0):
        self.__worker_id = id
        try:
            self.zk = KazooClient(hosts = '192.168.30.132:2181')
        except  Exception,e:
            print "connect"
        self.zk.start()
        #try:
        #    self.zk.start()
        #通知server

    def __del__(self):
        self.zk.stop()
        #通知server

    def wait2Work(self):
        if self.zk.exists("/master") == False:
            sleep_time = random.randint(1,5)
            time.sleep(sleep_time)
            return False
        else:
            return True

    def wait2Signal(self):
        signal = self.zk.get_children("/signal")
        print "get signal %s" % signal

    def plan1(self):
        if self.task_id == 9:
            self.zk.create("/stop")
        tasks = self.zk.get_children('/task')
        temp =  '/task/' + str(self.task_id)
        print temp
        mytask_data, mytask_stat = self.zk.get(temp)
        #mytask_data, mytask_stat = self.zk.get('/task/' + tasks[random.randint(1,len(tasks))])
        print "spider %d : task_is %s"%(self.__worker_id,  mytask_data.decode("utf-8"))
        self.zk.delete(temp)
        self.task_id += 2
        time.sleep(4)

    def doWork(self):

        if self.zk.exists("/workers") == False:
            self.zk.create("/workers")
        print "work1"
        self.zk.create("/workers/"+str(self.__worker_id),  ephemeral = True)
        print "work2"


        if self.zk.exists("/signal",watch = self.wait2Signal) == True:
            print "watch signal"
        
        while True:
            print "work!"
            self.plan1()
            if self.zk.exists("/stop") :
                return False

# first demo
logging.basicConfig()
demo = Kworker(id = 1)
while True:
    if demo.wait2Work() == True:
        break
while True:
    if demo.doWork() == False:
        break

