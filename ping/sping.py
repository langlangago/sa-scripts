#coding=utf8
import os
import sys
import commands
import string

def send_alarm(alarm_content):
    try:
        import socket
        host = 'alarmxxxx.com'
        results = socket.getaddrinfo(host,None)
        for result in results:
            print host, result[4][0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((result[4][0], 9001))
        import time
        time.sleep(2)

        json = '{"alarm_level":"%d","alarm_msg":"%s","alarm_type":"%d","ip":"%s","pid":"%d","pname":"%s","timestamp":"%d"}' % (2, alarm_content, 55, '127.0.0.1', 0, '佛山智慧城多线-01', time.time())
        print json

        length = len(json) + 8
        import struct
        send_buf = struct.pack("!I",length) + struct.pack("!I",696707) + json
        sock.send(send_buf)
        print repr(send_buf)
        #print sock.recv(1024)
        sock.close() 
    except Exception,ex:
        logger.info("%s:%s" % (Exception,ex))

if __name__ == '__main__':

	os.popen("date >> sping.log")
	dict={'11.11.11.11':'广州亚太双线-03','11.11.11.12':'北京亦庄双线-01','11.11.11.13':'无锡国际多线-01'}
	for i,k in dict.iteritems():
		os.popen("ping %s -c 400 -i 0.3|tail -3 >> sping.log"%i)
		lost=commands.getoutput("cat sping.log |tail -2 |sed -n '1p'|awk -F ',' '{print $3}'|cut -d' ' -f 2|sed 's/%//g'")
		avg=commands.getoutput("cat  sping.log |tail -1|awk -F ' ' '{print $4}'|cut -d '/' -f2")
		stat_str='[Ping Alarm] %s IP:%s Lost:%s%% Avg:%sms'%(k,i,lost,avg)
		if int(lost) > 3 :
			send_alarm(stat_str)
			#send_alarm("test by langxiaowei")
