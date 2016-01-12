#coding=utf8
import os
import sys
import commands
import string
import logging

def send_alarm(alarm_content, pname):
    try:
        import socket
        host = 'alarmxxx.com'
        results = socket.getaddrinfo(host,None)
        for result in results:
            print host, result[4][0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((result[4][0], 9001))
        import time
        time.sleep(2)

        eth0 = os.popen("ifconfig eth0 |grep 'inet addr'| cut -d: -f2|awk '{print $1}'")
        ip = eth0.read()

        json = '{"alarm_level":"%d","alarm_msg":"%s","alarm_type":"%d","ip":"%s","pid":"%d","pname":"%s","timestamp":"%d"}' % (2, alarm_content, 55, ip, 0, pname, time.time())
        print json

        length = len(json) + 8
        import struct
        send_buf = struct.pack("!I",length) + struct.pack("!I",696707) + json
        sock.send(send_buf)
        print repr(send_buf)
        #print sock.recv(1024)
        sock.close() 
    except Exception,ex:
        logging.info("%s:%s" % (Exception,ex))

if __name__ == '__main__':

	os.popen("date  >> sping.log")
	#send_alarm("Test By Langxiaowei","Open-Falcon")
	send_alarm(sys.argv[1],sys.argv[2])
