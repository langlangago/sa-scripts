# -*- encoding:utf-8 -*-

import MySQLdb
import commands
import sys
reload(sys)
sys.setdefaultencoding('utf8')




def getIp(idc_name):
	iplist = []
	db = MySQLdb.connect('11.11.11.11', 'root', 'adcd', 'weihui_sysop', charset='utf8')
	cursor = db.cursor()
	sql = "select ip from weihui_servers where idc_name = '%s'" % idc_name
	cursor.execute(sql)
	ips = cursor.fetchall()
	for ip in ips:
		iplist.append(ip[0]) 

	cursor.close()
	db.close()

	return iplist

def startAgent(ipList, idc_name):
	for ip in ipList:
		(stat1, out1) = commands.getstatusoutput('scp -P 32200 auto_agent.sh langxiaowei@%s:/home/langxiaowei' % (ip))
		if stat1 != 0:
			print ip, "\tError!!!", out1.decode("gbk")
			continue 
		(stat2, out2) = commands.getstatusoutput("ssh %s '/home/langxiaowei/auto_agent.sh %s %s'" % (ip, idc_name, ip))
		if stat2 !=0:
			print ip, "\tError!!!",out2.decode("gbk")
		else :
			print ip, "\tOK!"

def check_stat(ipList):
	print '......................'
	for ip in ipList:
		(stat, out) = commands.getstatusoutput("ssh %s '/data/services/falcon-agent/control status'" % ip )
		if stat !=0:
			print "check status error!",ip
		else:
			print "agent status: ",out

if __name__ == '__main__':
	idc_name = sys.argv[1]
	ipList = getIp(idc_name)
	startAgent(ipList, idc_name)
	check_stat(ipList)
