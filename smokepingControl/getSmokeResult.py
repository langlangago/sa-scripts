#!/usr/bin/python
#-*- encoding:utf-8 -*-

import commands
import os
import time

szFile = '/home/langxiaowei/smokeResult.txt'
ispList = ['telcom', 'unicom', 'CMCC', 'EDU']
rrd_basehome = '/var/lib/smokeping'

def makeFile():
	fd = open('/home/langxiaowei/smokeResult.txt','a')
	now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	fd.write('\n\n'+now)
	for isp in ispList:
		fd.write('\n\n'+isp+'\n\n')
		rrd_home = rrd_basehome+'/'+isp
		for paraent, dirs, files in os.walk(rrd_home):
			for file in files:
				(stat, out) = commands.getstatusoutput('rrdtool fetch %s/%s AVERAGE --start now-4hours > /home/langxiaowei/test' %(rrd_home, file))
				(stat1, out1) = commands.getstatusoutput('bash /home/langxiaowei/fetch_rrd.sh')
				(stat2, out2) = commands.getstatusoutput("grep -n1 %s /etc/smokeping/config.d/Targets |grep menu|awk '{print $NF}'" % file.split('.')[0])
				fd.write('\n'+out1+'\t\t'+out2+'\n')
	fd.close()


if __name__ =='__main__':
	makeFile()
