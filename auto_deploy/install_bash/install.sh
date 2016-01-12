#!/bin/bash

export pack_backup='/data/backup'
export pack_home='/data/services'
export bash_home='/data/install_bash'


if [ -z $2 ];then
	count=1
else
	count=$2
fi

#file_name=`ls -ltr $pack_backup | tail -1 |awk '{print $9}'`
#export pack_name=$(basename $file_name .tar.gz)
export pack_name=$(basename $1 .tar.gz)

cp $pack_backup/$pack_name.tar.gz $pack_home
if [ $? -ne 0 ] ; then
	echo "cp $pack_name error!"
	exit 1
fi

cd $pack_home && tar -zxf $pack_name.tar.gz && chmod 755 $pack_name && rm -rf $pack_name.tar.gz 

mkdir $pack_name/admin && mkdir $pack_name/var || exit 1

log=$pack_home/$pack_name/admin/start.log

pname=`ls $pack_name/bin/ |grep falcon`

echo "export bash_home='/data/install_bash'" >> $pack_home/$pack_name/admin/common-var.conf
echo "export pack_backup='/data/backup'" >> $pack_home/$pack_name/admin/common-var.conf
echo "export pack_home='/data/services'" >> $pack_home/$pack_name/admin/common-var.conf
echo "export install_path='$pack_home/$pack_name'" >> $pack_home/$pack_name/admin/common-var.conf
echo "export pack_name='$pack_name'" >> $pack_home/$pack_name/admin/common-var.conf
echo "export pname='$pname'" >> $pack_home/$pack_name/admin/common-var.conf
echo "export count='$count'" >> $pack_home/$pack_name/admin/common-var.conf
echo "0" > $pack_home/$pack_name/admin/auto_start.flag

cd $pack_name/bin || exit 1

for ((i=1;i<=$count;i++)); do
	echo "Start #$i"
	nohup ./$pname >> $log 2>&1 &
	sleep 2
done

echo `pidof $pname` > $pack_home/$pack_name/var/app.pid

pids=$(pidof $pname)
num=$(echo $pids|wc -w)

if [ $num -gt 0 ]; then
	echo "Start $pname OK!"
	bash $bash_home/init_bash.sh
	echo "# $pack_home/$pack_name app monitor" >> /etc/crontab
	echo "*/3 * * * * root $pack_home/$pack_name/admin/monitor.sh > $pack_home/$pack_name/admin/monitor.log 2>&1 &" >> /etc/crontab
	exit 0
else 
	echo "Start $pname Fail!"
	exit 1
fi



