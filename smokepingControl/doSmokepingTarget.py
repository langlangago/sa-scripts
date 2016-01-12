#!/usr/bin/python
# -*- encoding:utf-8 -*-
import pypinyin
from pypinyin import pinyin, lazy_pinyin
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

target = '/etc/smokeping/config.d/Targets'

def getIps(isp):
	ipList = {}
	db = MySQLdb.connect('11.11.11.11', 'root', 'abcd', 'weihui_sysop', charset='utf8')
	cursor = db.cursor()
	sql = "SELECT idc_name, %s_ip from weihui_idc_info where %s_ip != 'NONE' GROUP BY idc_id ORDER BY id" % (isp, isp)
	cursor.execute(sql)
	result = cursor.fetchall()
	for ip in result:
		ipList[ip[1]] = ip[0]

	cursor.close()
	db.close()
	return ipList

def doTarget(isp, ipList):

	fd =open(target,'a')

	if isp == 'tel':
		title = 'telcom'
		menu = '中国电信'
	elif isp == 'uni':
		title = 'unicom'
		menu = '中国联通'
	elif isp =='mob':
		title = 'CMCC'
		menu = '中国移动'
	else :
		title = 'EDU'
		menu = '中国教育'

	line = "+%s\nmenu = %s\ntitle = %s\n\n" % (title, menu, title)
	fd.writelines(line)

	for ip in ipList.keys():
		subTitle = ''.join(lazy_pinyin(ipList[ip]))+"-"+ip.split('.')[0]
		line2 = '++%s\nmenu = %s\ntitle = %s\nhost = %s\n\n' %(subTitle, ipList[ip].encode('utf8'), ip, ip)
		fd.writelines(line2)

	fd.close()

def doHead():
	fd =open(target,'w')
	line = """*** Targets ***
probe = FPing

menu = Top
title = Network Latency Grapher
remark = Welcome to the SmokePing website of xxx Company. \
Here you will learn all about the latency of our network.\n
"""
	fd.write(line)
	fd.close()

if __name__ == '__main__':
	doHead()
	isps =['tel', 'uni', 'mob', 'edu']
	for isp in isps:
		ipList = getIps(isp)
		doTarget(isp, ipList)
