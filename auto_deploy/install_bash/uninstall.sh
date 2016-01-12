#!/bin/bash

export pack_home='/data/services'
export pack_name=$(basename $1 .tar.gz)

#停止进程
bash $pack_home/$pack_name/admin/stop.sh || exit 1

sleep 2

#清除crontab

sed -i "/$pack_name/d" /etc/crontab

#删除包目录

rm -rf $pack_home/$pack_name

if [ -d $pack_home/$pack_name ] ;then
	echo "rm $pack_name failed"
	exit 1
else
	echo "uninstall $pack_name succeed"
	exit 0
fi

