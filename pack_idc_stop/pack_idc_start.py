#!/usr/bin/python
#-*-coding:utf8-*-

import urllib2
import json
import os
import sys

vid = []
real_host = {}
real_match = {}

def ip_into_int(ip):
	return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
	ip = ip_into_int(ip)
	net_a = ip_into_int('10.255.255.255') >> 24
	net_b = ip_into_int('172.31.255.255') >> 20
	net_c = ip_into_int('192.168.255.255') >> 16
	return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c


def match_idc(real_host, hname):

	for key in real_host.keys():
		match_ip = []
		t3 = len(real_host[key])

		for n in range(t3):
			name_url = 'http://www.domain.com/xxx/getIdcByIp.do?ip=%s' % real_host[key][n]
			name = urllib2.urlopen(name_url)
			name_json = json.loads(name.read())
			if name_json['object']['name'] == hname:
				match_ip.append(real_host[key][n])
				
		if len(match_ip) != 0:
			real_match[key]=match_ip

	name.close()
	return real_match


def get_ips(vid):

	t = len(vid)
	for i in range(t):
		host_ip = []
		ips_url = 'http://www.domain.com/cutVersinIntanceIP.do?versionId=%d ' % vid[i]
		ips =urllib2.urlopen(ips_url)
		ips_json = json.loads(ips.read())

		t2 = len(ips_json['object'])
		for k in range(t2):
			flag = 0
			ip_list = ips_json['object'][k].split(',')

			t3 =len(ip_list)
			for m in range(t3):
				if flag ==0 and is_internal_ip(ip_list[m]) == False:
					host_ip.append(ip_list[m])
					flag = 1
					
		real_host[vid[i]] = host_ip

	ips.close()
	return real_host


def get_vid(pname):

	vid_url = 'http://www.domain.com/xxx/listVersion.do?name=%s' % pname
	html = urllib2.urlopen(vid_url)
	hjson = json.loads(html.read())

	t = len(hjson['object'])
	if t == 0:
		print "...................."
		print "%s is not exist,please check the pack_name !!!" % pname
		print "all pack start faild !!"
		sys.exit()
	for i in range(t):
		count = hjson['object'][i]['count']
		if count > 0:
			vid.append(hjson['object'][i]['versionId'])
	html.close()
	
	return vid


def start_pack(real_match):

	for x in real_match.keys():
		start_url = 'http://www.domain.com/xxx/start.do?ips=%s&versionId=%s&key=xxxxxxxxxx&retry=no&timeOut=240&executeType=0&interval=30&operator=dw_%s' % (",".join(real_match[x]), x,os.getlogin())
		start_html = urllib2.urlopen(start_url)
		start_json = json.loads(start_html.read())

		task_url = 'http://www.domain.com/xxx/getDetailInfoByTaskId.do?task_id=%s' % start_json['object']['taskId']
		task_html = urllib2.urlopen(task_url)
		task_json = json.loads(task_html.read())

		if start_json['code'] == 0:
			print "package %s start success!" % task_json['object'][0]['package_name']
		else:
			print "package %s start error!" % task_json['object'][0]['package_name']

		start_html.close()
		task_html.close()
		

if __name__=='__main__':
	if len(sys.argv) != 2:
		print "Usage:  python   pack_stop.py    xxxx.json"
		sys.exit()

	with open(sys.argv[1]) as f:
		data = f.read()
	pack_idc = json.loads(data)
	
	t = len(pack_idc['pack_name'])
	hname = pack_idc['idc_name']
	for n in range(t):
		pname = pack_idc['pack_name'][n]
		print "starting %s on %s ...... " % (pname, hname)
		vid = get_vid(pname)
	print '..............'
	real_host = get_ips(vid)
	real_match = match_idc(real_host, hname)
	start_pack(real_match)
