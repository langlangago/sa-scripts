def ip_into_int(ip):
	return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
	ip = ip_into_int(ip)
	net_a = ip_into_int('10.255.255.255') >> 24
	net_b = ip_into_int('172.31.255.255') >> 20
	net_c = ip_into_int('192.168.255.255') >> 16
	return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

if __name__ == '__main__':
	ip = '192.168.0.1'
	print ip, is_internal_ip(ip)
	ip = '10.20.160.56'
	print ip, is_internal_ip(ip)
	ip = '172.16.1.1'
	print ip, is_internal_ip(ip)

