#!/usr/bin/python
# -*- encoding:utf-8 -*-

import commands
import time
import json

def packData(host, ip, rrt, lost):
	resource_d = {
		'fping.rrt':[rrt, 'GAUGE'],
		'fping.lost':[lost, 'GAUGE']
	}

	output = []
	for resource in resource_d.keys():
		t = {}
		t['endpoint'] = host
		t['timestamp'] = int(time.time())
		t['step'] = 60
		t['counterType'] = resource_d[resource][1]
		t['metric'] = resource
		t['value'] = resource_d[resource][0]
		t['tags'] = "ip=%s" % ip

		output.append(t)
	return output
		


def fping(ipFile):
	with open('/data/open-falcon/agent/cfg.json') as f:
            d = json.load(f)
            host = d['hostname']
	result = []
	cmd = 'sudo fping -c 20 -q -B1 -r1 -i10 -f %s' % ipFile
	(stat, out) = commands.getstatusoutput(cmd)
#	if stat!= 0:
#		print out
#		return
	result = out.split('\n')
	output2 = []
	for line in result:
		(stat2, ip) = commands.getstatusoutput("echo %s|awk '{print $1}'" % line)
		if len(line) > 45:
			(stat3, rtt) = commands.getstatusoutput("echo %s|awk -F'/' '{print $NF}'" % line)
			(stat4, lost) = commands.getstatusoutput("echo %s|awk -F'%%' '{print $2}'|awk -F'/' '{print $NF}'" % line)
			pack = packData(host, ip, rtt, lost)
			output2 = output2 + pack
		else:
			pack = packData(host, ip, 0, 100)
			output2 = output2 + pack
	return output2




if __name__ == '__main__':
	d = fping('/data/open-falcon/agent/plugin/common/hosts.txt')
	if d:
		print json.dumps(d)
