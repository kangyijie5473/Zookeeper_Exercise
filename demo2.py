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
            self.zk = KazooClient(hosts = hosts_list)
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
        if self.zk.exists("/master") == None:
            sleep_time = random.randint(1,5)
            time.sleep(sleep_time)
            return False
        else:
            return True

    def wait2Signal(self):
        signal = self.zk.get_children("/signal")
        print "get signal %s" % signal

    def plan1(self):

        if self.task_id == 29:
            self.zk.create("/stop")

        tasks = self.zk.get_children('/task')
        #obj_tasks = '/task/' + tasks[random.randint(1,len(tasks))]
        obj_tasks = '/task/1001'
        mytask_data, mytask_stat = self.zk.get(obj_tasks)

        #mo ni chu li ren wu 
        print "spider %d : task_is %s"%(self.__worker_id,  mytask_data.decode("utf-8"))

        # chu li wan cheng 
        self.zk.delete(obj_tasks)

        self.task_id += 2
        time.sleep(4)

    def doWork(self):

        if self.zk.exists("/workers") == None:
            self.zk.create("/workers")
 		
 		# zhu ci id --> yong lai jian kong spider shi fou cun huo
        self.zk.create("/workers/"+str(self.__worker_id),  ephemeral = True)



        if self.zk.exists("/signal",watch = self.wait2Signal):
            print "watch signal"
        
        while True:
        	# work plan No 1
            self.plan1()

            # /stop --> stop all workers
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

