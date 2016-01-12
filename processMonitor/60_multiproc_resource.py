#!/usr/bin/python
#-*- coding:utf-8 -*-
#此脚本仅支持多个同样进程名的进程监控pname_port

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
    def __init__(self, pname, pid, pport):
        #self.host = socket.gethostname()
        with open('/home/langxiaowei/falcon-agent/cfg.json') as f:
            d = json.load(f)
        self.host = d['hostname']
        self.pid = pid
        self.pname = pname
        self.port = pport

    def get_cpu_user(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $14+$16}'"
        return os.popen(cmd).read().strip("\n")

    def get_cpu_sys(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $15+$17}'"
        return os.popen(cmd).read().strip("\n")

    def get_cpu_all(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $14+$15+$16+$17}'"
        return os.popen(cmd).read().strip("\n")

    def get_mem(self):
        cmd="cat /proc/" + str(self.pid)  +  "/status |grep VmRSS |awk '{print $2*1024}'"
        return os.popen(cmd).read().strip("\n")

    def get_swap(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $(NF-7)+$(NF-8)}' "
        return os.popen(cmd).read().strip("\n")

    def get_fd(self):
        cmd="cat /proc/" + str(self.pid)  +  "/status |grep FDSize |awk '{print $2}'"
        return os.popen(cmd).read().strip("\n")

    def get_state(self):
		cmd="cat /proc/" + str(self.pid) + "/stat |awk '{print $3}'"
		return ord(os.popen(cmd).read().strip("\n"))

    def run(self):
        self.resources_d={
            'process.cpu.user':[self.get_cpu_user,'COUNTER'],
            'process.cpu.sys':[self.get_cpu_sys,'COUNTER'],
            'process.cpu.all':[self.get_cpu_all,'COUNTER'],
            'process.mem':[self.get_mem,'GAUGE'],
            'process.swap':[self.get_swap,'GAUGE'],
            'process.fd':[self.get_fd,'GAUGE'],
			'process.state':[self.get_state,'GAUGE']
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
                t['tags'] = 'pname=%s_%s' % (self.pname, self.port)
                output.append(t)
        return output

    def dump_data(self):
        return json.dumps()

if __name__ == "__main__":
	pname_dict = {}
	d_list = []

	pnames = os.popen("sudo find /data/services -iname common-var.conf | xargs grep -i 'app_name' |awk '{print $2}'|cut -d'\"' -f 2  2>&1 ") 
	for i in pnames.readlines():
		pname = i.strip('\n')
		pids =os.popen("pidof '%s'" % pname)
		pid = pids.read().strip('\n').split(' ')
		if len(pid) < 2:
			continue
		for p in pid:
			pname_dict[p] = pname
	for key,value in pname_dict.items():
		if 0 < len(key) < 6:
			port = os.popen("netstat -tlnp|grep %s | tail -1|awk '{print $4}'|awk -F':' '{print $NF}'" % key)
			pport = port.read().strip('\n')
			d = Resource(value, int(key), int(pport)).run()
			d_list = d_list + d
	print json.dumps(d_list)
