#!/usr/bin/python
# -*- encoding:utf-8 -*-
import urllib2
import json
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getPages():
	ip_url = 'http://www.cmdb.com/server/list.do?buss=000000023555&page=1'
	ip_html = urllib2.urlopen(ip_url)
	ip_json = json.loads(ip_html.read())
	ip_html.close()
	total = ip_json['object']['count']
	#perPageCount = 20
	pages = (total+20-1)/20
	return pages

def getIdcInfo(pages):
	db = MySQLdb.connect("127.0.0.1", "root", "weihui@2015", "weihui_sysop", charset = "utf8")
	cursor = db.cursor()
	
	for i in range(1, pages+1):
		ip_url = 'http://www.cmdb.com/server/list.do?buss=000000023555&page=%s' % i
		ip_html = urllib2.urlopen(ip_url)
		ip_json = json.loads(ip_html.read())
		ip_html.close()
		lists = ip_json['object']['lists']
		count = len(lists)
		for m in range(0, count):

			idc_id = lists[m]['idc_id']
			idc_name = lists[m]['idc_name']
			default_ip = lists[m]['default_ip']
			tel_ip = lists[m]['tel_ip']
			uni_ip = lists[m]['uni_ip']
			mob_ip = lists[m]['mob_ip']
			edu_ip = lists[m]['edu_ip']
			bgp_ip = lists[m]['bgp_ip']
			hk_ip = lists[m]['hk_ip']
			in_ip = lists[m]['in_ip']
			smn_ip = lists[m]['smn_ip']
			other_ip = lists[m]['other_ip']
			os_name = lists[m]['os_name']
			status_name = lists[m]['status_name']
			server_type_name = lists[m]['server_type_name']
			dw_tech_admin = lists[m]['dw_tech_admin']
			buss_name = lists[m]['buss_name']
			
			sql = " insert into weihui_idc_info values('',%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (idc_id, idc_name, default_ip, tel_ip, uni_ip, mob_ip, edu_ip, bgp_ip, hk_ip, in_ip, smn_ip, other_ip, os_name, status_name, server_type_name, dw_tech_admin, buss_name)
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()


	cursor.close()
	db.close()

def create_table():
	db = MySQLdb.connect("127.0.0.1", "root", "abcd", "weihui_sysop", charset = "utf8")
	cursor = db.cursor()

	cursor.execute("DROP TABLE IF EXISTS weihui_idc_info")
	sql= """ create table weihui_idc_info(
		id	int(20) not null AUTO_INCREMENT,
		idc_id	int(20) not null,
		idc_name varchar(255) not null,
		default_ip varchar(255) not null,
		tel_ip varchar(255) default null,
		uni_ip varchar(255) default null,
		mob_ip varchar(255) default null,
		edu_ip varchar(255) default null,
		bgp_ip varchar(255) default null,
		hk_ip varchar(255) default null,
		in_ip varchar(255) default null,
		smn_ip varchar(255) default null,
		other_ip varchar(255) default null,
		os_name varchar(255),
		status_name varchar(255),
		server_type_name varchar(255),
		dw_tech_admin varchar(255),
		buss_name varchar(255),
		PRIMARY KEY(id)
		) AUTO_INCREMENT=1 DEFAULT charset= utf8;
		"""
	cursor.execute(sql)
	cursor.close()
	db.close()

if __name__ == '__main__':
	create_table()
	pages = getPages()
	getIdcInfo(pages)
	
