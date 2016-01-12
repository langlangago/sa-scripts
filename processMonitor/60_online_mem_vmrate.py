#! /usr/bin/python
#-*- coding:utf-8 -*-

from __future__ import division
import os,sys
import os.path
from os.path import isfile
from traceback import format_exc
import xmlrpclib
import socket
import time
import json
import copy

class Resource():
    def __init__(self, pname, pid):
        with open('/home/langxiaowei/falcon-agent/cfg.json') as f:
			d = json.load(f)
        self.host = d['hostname']
        self.pid = pid
        self.pname = pname

    def get_VmSize(self):
        cmd="cat /proc/" + str(self.pid)  +  "/status |grep VmSize |awk '{print $2}'"
        return int(os.popen(cmd).read().strip("\n"))/1024*1000000

    def get_VmRSS(self):
        cmd="cat /proc/" + str(self.pid)  +  "/status |grep VmRSS |awk '{print $2}'"
        return int(os.popen(cmd).read().strip("\n"))/1024*1000000

    def get_vm_used_percent(self):
        percent = int(self.get_VmRSS())/int(self.get_VmSize()) * 100
        rate = float('%.2f ' % percent)
        return rate

    def run(self):
        self.resources_d={
            'process.VmSize':[self.get_VmSize,'GAUGE'],
            'process.VmRSS':[self.get_VmRSS,'GAUGE'],
            'process.Vm_Used_Percent':[self.get_vm_used_percent,'GAUGE']
        }

        if not os.path.isdir("/proc/" + str(self.pid)):
            return

        output = []
        for resource in  self.resources_d.keys():
                t = {}
                t['endpoint'] = self.host
                t['timestamp'] = int(time.time())
                t['step'] = 60
                t['counterType'] = self.resources_d[resource][1]
                t['metric'] = resource
                t['value']= self.resources_d[resource][0]()
                t['tags'] = 'pname=%s' %self.pname

                output.append(t)

        return output

    def dump_data(self):
        return json.dumps()

if __name__ == "__main__":
    pname = 'nmob_online_mem_d'
    pid = os.popen("pidof %s" % pname).read().strip('\n') 
    d = Resource(pname, pid).run()
    if d:
        print json.dumps(d)
