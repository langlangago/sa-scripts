
#source $pack_home/$pack_name/admin/common-var.conf

pack_home=/data/services
pack_name=falcon-agent-1.0.0
pname=falcon-agent

#��ʼ����־�ļ�

#�����������

pids=$(pidof $pname)

if [ -z "$pids" ] ; then
	echo "no running $pname found,already stoped"
	exit 0
fi

#ֹͣ����

for i in $pids ; do
	echo "kill $pname pid=$i"
	kill $i
	sleep 5
done

#����ȷ��

if [ -z "$(pidof $pname)" ] ; then
	echo "stop $pname ok,all $pname got killed"
	echo "1" > $pack_home/$pack_name/admin/auto_start.flag
	exit 0
else
	echo "stop $pname failed,found $pname still running."
	pidof $pname |xargs -f -ps -lf
	#tail -n 20 $log
	exit 1
fi
